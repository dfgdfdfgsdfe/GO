import random


def candidate_moves(board, limit=40):
    candidates = []

    for x in range(board.size):
        for y in range(board.size):

            if board.board[x, y] != 0:
                continue

            nearby = False

            for nx, ny in board.neighbors(x, y):
                if board.board[nx, ny] != 0:
                    nearby = True
                    break

            if nearby:
                candidates.append((x, y))

    if not candidates:
        for x in range(board.size):
            for y in range(board.size):
                if board.board[x, y] == 0:
                    candidates.append((x, y))

    random.shuffle(candidates)

    return candidates[:limit]
