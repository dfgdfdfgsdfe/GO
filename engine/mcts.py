import math
import random
import time

from engine.board import BLACK, WHITE, EMPTY


class Node:

    def __init__(self, board, parent=None, move=None):

        self.board = board
        self.parent = parent
        self.move = move

        self.children = []

        self.visits = 0
        self.wins = 0

    def ucb1(self, c=1.4):

        if self.visits == 0:
            return float("inf")

        return (
            self.wins / self.visits
            +
            c * math.sqrt(
                math.log(self.parent.visits + 1)
                / self.visits
            )
        )


class MCTS:

    def __init__(self, max_time=2.5, rollout_depth=60):

        self.max_time = max_time
        self.rollout_depth = rollout_depth

    # -----------------------------
    # 후보 수 생성 (핵심 강화)
    # -----------------------------
    def get_candidates(self, board):

        moves = []

        center = board.size // 2

        for x in range(board.size):
            for y in range(board.size):

                if board.board[x, y] != EMPTY:
                    continue

                score = 0

                # 중앙 선호
                score -= abs(x - center) + abs(y - center)

                # 주변 돌 있으면 + (전투 유도)
                for nx, ny in board.neighbors(x, y):
                    if board.board[nx, ny] != EMPTY:
                        score += 5

                # 잡을 수 있는 수 우선
                temp = board.copy()
                temp.place_stone(x, y)

                captured = (
                    board.black_captures + board.white_captures
                )

                if captured > 0:
                    score += 50

                moves.append((score, (x, y)))

        moves.sort(reverse=True, key=lambda x: x[0])

        return [m[1] for m in moves[:20]]  # ⭐ 핵심: 20개만 탐색

    # -----------------------------
    # 선택
    # -----------------------------
    def select(self, node):

        while node.children:

            node = max(node.children, key=lambda n: n.ucb1())

        return node

    # -----------------------------
    # 확장
    # -----------------------------
    def expand(self, node):

        moves = self.get_candidates(node.board)

        for x, y in moves:

            temp = node.board.copy()

            if temp.place_stone(x, y):

                child = Node(temp, node, (x, y))
                node.children.append(child)

    # -----------------------------
    # rollout (강화됨)
    # -----------------------------
    def simulate(self, board):

        temp = board.copy()

        for _ in range(self.rollout_depth):

            moves = self.get_candidates(temp)

            if not moves:
                break

            # 상위 5개 중 선택 (랜덤성 + 질)
            move = random.choice(moves[:5])

            temp.place_stone(move[0], move[1])

        black = temp.black_captures
        white = temp.white_captures

        return BLACK if black >= white else WHITE

    # -----------------------------
    # backprop
    # -----------------------------
    def backpropagate(self, node, winner, root_color):

        while node:

            node.visits += 1

            if winner == root_color:
                node.wins += 1

            node = node.parent

    # -----------------------------
    # search
    # -----------------------------
    def search(self, board):

        root = Node(board.copy())
        root_color = board.turn

        self.expand(root)

        start = time.time()

        while time.time() - start < self.max_time:

            node = self.select(root)

            if node.visits > 0:
                self.expand(node)

                if node.children:
                    node = random.choice(node.children)

            winner = self.simulate(node.board)

            self.backpropagate(node, winner, root_color)

        best = max(root.children, key=lambda n: n.visits)

        winrate = best.wins / max(best.visits, 1)

        return best.move, winrate
