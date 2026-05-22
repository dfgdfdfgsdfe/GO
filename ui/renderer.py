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

    fig, ax = plt.subplots(
        figsize=(9, 9)
    )

    ax.set_facecolor("#DEB887")

    # 가로선
    for i in range(board.size):

        ax.plot(
            [0, board.size - 1],
            [i, i],
            color="black"
        )

    # 세로선
    for i in range(board.size):

        ax.plot(
            [i, i],
            [0, board.size - 1],
            color="black"
        )

    # 화점
    for x, y in STAR_POINTS:

        ax.scatter(
            y,
            x,
            s=20,
            color="black"
        )

    # 돌 그리기
    for x in range(board.size):

        for y in range(board.size):

            stone = board.board[x, y]

            if stone == BLACK:

                ax.scatter(
                    y,
                    x,
                    s=300,
                    color="black"
                )

            elif stone == WHITE:

                ax.scatter(
                    y,
                    x,
                    s=300,
                    color="white",
                    edgecolors="black"
                )

    ax.set_xlim(-1, board.size)

    ax.set_ylim(
        board.size,
        -1
    )

    ax.set_xticks([])

    ax.set_yticks([])

    return fig
