import math
import random
import time

from engine.board import BLACK
from engine.scoring import score_game


class Node:

    def __init__(
        self,
        board,
        parent=None,
        move=None
    ):

        self.board = board

        self.parent = parent

        self.move = move

        self.children = []

        self.visits = 0

        self.wins = 0

    def ucb1(self, c=1.4):

        if self.visits == 0:

            return float("inf")

        exploitation = (
            self.wins / self.visits
        )

        exploration = (
            c *
            math.sqrt(
                math.log(self.parent.visits + 1)
                /
                self.visits
            )
        )

        return exploitation + exploration


class MCTS:

    def __init__(
        self,
        min_time=0,
        max_time=3,
        rollout_depth=30
    ):

        self.min_time = min_time

        self.max_time = max_time

        self.rollout_depth = rollout_depth

    def valid_moves(self, board):

        moves = []

        for x in range(board.size):

            for y in range(board.size):

                temp = board.copy()

                if temp.place_stone(x, y):

                    moves.append((x, y))

        random.shuffle(moves)

        return moves[:40]

    def select(self, node):

        while node.children:

            node = max(
                node.children,
                key=lambda n: n.ucb1()
            )

        return node

    def expand(self, node):

        moves = self.valid_moves(
            node.board
        )

        for move in moves:

            temp = node.board.copy()

            temp.place_stone(
                move[0],
                move[1]
            )

            child = Node(
                temp,
                parent=node,
                move=move
            )

            node.children.append(child)

    def simulate(self, board):

        temp = board.copy()

        for _ in range(
            self.rollout_depth
        ):

            moves = self.valid_moves(temp)

            if not moves:

                break

            move = random.choice(moves)

            temp.place_stone(
                move[0],
                move[1]
            )

        black_score, white_score = (
            score_game(temp)
        )

        if black_score > white_score:

            return BLACK

        return 2

    def backpropagate(
        self,
        node,
        winner,
        root_color
    ):

        while node:

            node.visits += 1

            if winner == root_color:

                node.wins += 1

            node = node.parent

    def search(self, board):

        root = Node(board.copy())

        root_color = board.turn

        self.expand(root)

        if not root.children:

            return None, 0.5

        think_time = random.uniform(
            self.min_time,
            self.max_time
        )

        start = time.time()

        while (
            time.time() - start
            <
            think_time
        ):

            node = self.select(root)

            if node.visits > 0:

                self.expand(node)

                if node.children:

                    node = random.choice(
                        node.children
                    )

            winner = self.simulate(
                node.board
            )

            self.backpropagate(
                node,
                winner,
                root_color
            )

        best = max(
            root.children,
            key=lambda n: n.visits
        )

        winrate = (
            best.wins
            /
            max(best.visits, 1)
        )

        return best.move, winrate
