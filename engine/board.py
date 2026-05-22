import numpy as np
from copy import deepcopy

EMPTY = 0
BLACK = 1
WHITE = 2

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


class GoBoard:

    def __init__(self, size=19):

        self.size = size

        self.board = np.zeros(
            (size, size),
            dtype=np.int8
        )

        self.turn = BLACK

        self.previous_position = None

        self.move_history = []

        self.passes = 0

        self.black_captures = 0
        self.white_captures = 0

    def copy(self):

        return deepcopy(self)

    def in_bounds(self, x, y):

        return (
            0 <= x < self.size
            and
            0 <= y < self.size
        )

    def neighbors(self, x, y):

        for dx, dy in DIRECTIONS:

            nx = x + dx
            ny = y + dy

            if self.in_bounds(nx, ny):

                yield nx, ny

    def get_group(self, x, y):

        color = self.board[x, y]

        if color == EMPTY:

            return set()

        stack = [(x, y)]

        visited = set()

        while stack:

            cx, cy = stack.pop()

            if (cx, cy) in visited:

                continue

            visited.add((cx, cy))

            for nx, ny in self.neighbors(cx, cy):

                if self.board[nx, ny] == color:

                    stack.append((nx, ny))

        return visited

    def liberties(self, group):

        libs = set()

        for x, y in group:

            for nx, ny in self.neighbors(x, y):

                if self.board[nx, ny] == EMPTY:

                    libs.add((nx, ny))

        return libs

    def remove_group(self, group):

        if not group:

            return

        color = self.board[next(iter(group))]

        for x, y in group:

            self.board[x, y] = EMPTY

        if color == BLACK:

            self.white_captures += len(group)

        else:

            self.black_captures += len(group)

    def place_stone(self, x, y):

        if not self.in_bounds(x, y):

            return False

        if self.board[x, y] != EMPTY:

            return False

        backup = self.board.copy()

        self.board[x, y] = self.turn

        opponent = (
            BLACK
            if self.turn == WHITE
            else WHITE
        )

        for nx, ny in self.neighbors(x, y):

            if self.board[nx, ny] == opponent:

                group = self.get_group(nx, ny)

                if len(self.liberties(group)) == 0:

                    self.remove_group(group)

        own_group = self.get_group(x, y)

        if len(self.liberties(own_group)) == 0:

            self.board = backup

            return False

        self.move_history.append(
            (x, y, self.turn)
        )

        self.turn = opponent

        self.passes = 0

        return True

    def pass_turn(self):

        self.passes += 1

        self.turn = (
            BLACK
            if self.turn == WHITE
            else WHITE
        )

    def game_over(self):

        return self.passes >= 2
