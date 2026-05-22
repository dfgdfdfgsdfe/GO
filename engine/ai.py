from engine.mcts import MCTS


class GoAI:

    def __init__(self):

        self.mcts = MCTS(
            max_time=2.5,
            rollout_depth=60
        )

    def select_move(self, board):

        return self.mcts.search(board)
