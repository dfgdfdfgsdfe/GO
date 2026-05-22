from engine.mcts import MCTS


class GoAI:

    def __init__(self):

        self.mcts = MCTS(
            min_time=0,
            max_time=2,
            rollout_depth=20
        )

    def select_move(self, board):

        return self.mcts.search(board)
