import matplotlib.pyplot as plt

from engine.board import BLACK, WHITE


STAR_POINTS = [
    (3, 3),
    (3, 9),
    (3, 15),
    (9, 3),
    (9, 9),
    (9, 15),
    (15, 3),
    (15, 9),
    (15, 15),
]


def render_board(board):
    fig, ax = plt.subplots(figsize=(9, 9))

    ax.set_facecolor('#DEB887')

    for i in range(board.size):
        ax.plot([0, 18], [i, i], color='black')
        ax.plot([i, i], [0, 18], color='black')

    for x
