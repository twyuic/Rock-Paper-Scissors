import random
import numpy as np
from sklearn.linear_model import SGDClassifier

model = SGDClassifier(loss="log_loss", max_iter=5, tol=None)
trained = False
history_X, history_y = [], []

def player(prev_play, opponent_history=[]):
    global model, trained, history_X, history_y

    moves = ["R", "P", "S"]
    move_map = {"R":0, "P":1, "S":2}
    move_map_rev = {0:"R", 1:"P", 2:"S"}

    if prev_play == "":
        return random.choice(moves)

    opponent_history.append(prev_play)
    n = len(opponent_history)

    if n < 4:
        return random.choice(moves)

    # pre training data
    N = 3
    if n > N:
        seq = opponent_history[-N-1:-1]
        if all(m in move_map for m in seq):
            X = [move_map[m] for m in seq]
            y = move_map[prev_play]
            history_X.append(X)
            history_y.append(y)

            if len(history_y) >= 20:  # data
                model.partial_fit([X], [y], classes=[0,1,2])
                trained = True

    # prediction
    preds = []

    # ml
    if trained:
        recent = [move_map[m] for m in opponent_history[-N:]]
        preds.append(model.predict([recent])[0])

    # pattern(2-5)
    for length in range(2, 6):
        if n >= length:
            last_seq = "".join(opponent_history[-length:])
            for i in range(n - length):
                seq = "".join(opponent_history[i:i+length])
                if seq == last_seq:
                    preds.append(move_map[opponent_history[i+length]])

    # last 20
    recent = opponent_history[-20:]
    if recent:
        counts = {"R": recent.count("R"), "P": recent.count("P"), "S": recent.count("S")}
        most = max(counts, key=counts.get)
        preds.append(move_map[most])

    # vote
    if preds:
        predicted = max(set(preds), key=preds.count)
    else:
        predicted = random.choice([0,1,2])

    # against
    counter_map = {0:1, 1:2, 2:0}
    counter_move = counter_map[predicted]


    if random.random() < 0.005:
        counter_move = random.choice([0,1,2])

    return move_map_rev[counter_move]

# i dnot like you, Abbey.