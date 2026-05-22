import numpy as np

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

    def is_legal(self, x, y):
        temp = self.copy()
        return temp.place_stone(x, y)

    def place_stone(self, x, y):
        if not self.in_bounds(x, y):
            return False

        if self.board[x, y] != EMPTY:
            return False

        backup = self.board.copy()
        previous_backup = None

        if self.previous_position is not None:
            previous_backup = self.previous_position.copy()

        self.previous_position = self.board.copy()

        self.board[x, y] = self.turn

        opponent = BLACK if self.turn == WHITE else WHITE

        for nx, ny in self.neighbors(x, y):
            if self.board[nx, ny] == opponent:
                group = self.get_group(nx, ny)

                if len(self.liberties(group)) == 0:
                    self.remove_group(group)

        own_group = self.get_group(x, y)

        if len(self.liberties(own_group)) == 0:
            self.board = backup
            self.previous_position = previous_backup
            return False

        if self.previous_position is not None:
            if np.array_equal(self.previous_position, self.board):
                self.board = backup
                self.previous_position = previous_backup
                return False

        self.move_history.append((x, y, self.turn))

        self.turn = opponent
        self.passes = 0

        return True

    def pass_turn(self):
        self.passes += 1
        self.turn = BLACK if self.turn == WHITE else WHITE

    def game_over(self):
        return self.passes >= 2
