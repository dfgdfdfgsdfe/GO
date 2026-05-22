from engine.board import BLACK, WHITE, EMPTY

KOMI = 6.5


def flood_fill(board, x, y, visited):
    stack = [(x, y)]
    region = set()

    while stack:
        cx, cy = stack.pop()

        if (cx, cy) in visited:
            continue

        visited.add((cx, cy))
        region.add((cx, cy))

        for nx, ny in board.neighbors(cx, cy):
            if board.board[nx, ny] == EMPTY:
                stack.append((nx, ny))

    return region


def territory_owner(board, region):
    neighbors = set()

    for x, y in region:
        for nx, ny in board.neighbors(x, y):
            color = board.board[nx, ny]

            if color != EMPTY:
                neighbors.add(color)

    if len(neighbors) == 1:
        return next(iter(neighbors))

    return None


def score_game(board):
    black = board.black_captures
    white = board.white_captures + KOMI

    visited = set()

    for x in range(board.size):
        for y in range(board.size):
            value = board.board[x, y]

            if value == BLACK:
                black += 1

            elif value == WHITE:
                white += 1

            else:
                if (x, y) not in visited:
                    region = flood_fill(board, x, y, visited)
                    owner = territory_owner(board, region)

                    if owner == BLACK:
                        black += len(region)
                    elif owner == WHITE:
                        white += len(region)

    return black, white
