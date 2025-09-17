import random

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)
    moves = ["R", "P", "S"]
    n = len(opponent_history)

    if n < 2:
        return random.choice(moves)

    pattern_scores = {}

    # 多步模式匹配 1~4 步，長度 2,3 步給高權重
    for length in range(1, 5):
        if n >= length:
            last_seq = "".join(opponent_history[-length:])
            for i in range(n - length):
                seq = "".join(opponent_history[i:i+length])
                next_move = opponent_history[i+length]
                if seq == last_seq:
                    weight = 0.7 if length in [2,3] else 0.3
                    pattern_scores[next_move] = pattern_scores.get(next_move, 0) + weight

    # 最近 8~18 手出手頻率加權
    recent = opponent_history[-18:]
    counts = {"R": recent.count("R"), "P": recent.count("P"), "S": recent.count("S")}
    for move in moves:
        pattern_scores[move] = pattern_scores.get(move, 0) + counts[move] * 0.2

    # 預測下一手
    if pattern_scores:
        predicted = max(pattern_scores, key=pattern_scores.get)
    else:
        predicted = random.choice(moves)

    counter_map = {"R":"P", "P":"S", "S":"R"}
    counter_move = counter_map[predicted]

    # 動態隨機化，避免 Abbey 完全抓到
    if n > 20 and random.random() < 0.05:
        return random.choice(moves)
    elif n > 10 and random.random() < 0.02:
        return random.choice(moves)

    return counter_move
