import math

        for _ in range(self.rollout_depth):
            move = self.rollout_policy(temp)

            if move is None:
                temp.pass_turn()
                break

            temp.place_stone(*move)

        black, white = score_game(temp)

        return BLACK if black > white else WHITE

    def backpropagate(self, node, winner, root_color):
        while node:
            node.visits += 1

            if winner == root_color:
                node.wins += 1

            node = node.parent

    def parallel_rollout(self, node, root_color):
        winner = self.simulate(node.board)
        return node, winner, root_color

    def search(self, board):
        root = Node(board.copy())

        root_color = board.turn

        self.expand(root)

        if not root.children:
            return None, 0.5

        think_time = random.uniform(self.min_time, self.max_time)

        start = time.time()

        with ThreadPoolExecutor(max_workers=4) as executor:

            while time.time() - start < think_time:

                tasks = []

                for _ in range(4):
                    node = self.select(root)

                    if node.visits > 0:
                        self.expand(node)

                        if node.children:
                            node = random.choice(node.children)

                    tasks.append(
                        executor.submit(
                            self.parallel_rollout,
                            node,
                            root_color
                        )
                    )

                for task in tasks:
                    node, winner, color = task.result()
                    self.backpropagate(node, winner, color)

        best = max(root.children, key=lambda n: n.visits)

        winrate = best.wins / max(best.visits, 1)

        return best.move, winrate
