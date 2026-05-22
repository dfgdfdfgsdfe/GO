import matplotlib.pyplot as plt

from engine.board import BLACK, WHITE


def render_board(board):

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.set_facecolor("#DEB887")

    size = board.size

    # -------------------------
    # 바둑판 선
    # -------------------------
    for i in range(size):

        ax.plot([0, size - 1], [i, i], color="black")
        ax.plot([i, i], [0, size - 1], color="black")

    # -------------------------
    # 화점
    # -------------------------
    star_points = [
        (3, 3), (3, 9), (3, 15),
        (9, 3), (9, 9), (9, 15),
        (15, 3), (15, 9), (15, 15),
    ]

    for x, y in star_points:

        ax.scatter(y, x, s=20, color="black")

    # -------------------------
    # 돌
    # -------------------------
    for x in range(size):

        for y in range(size):

            stone = board.board[x, y]

            if stone == BLACK:

                ax.scatter(y, x, s=300, color="black")

            elif stone == WHITE:

                ax.scatter(y, x, s=300, color="white", edgecolors="black")

    # -------------------------
    # ⭐ 좌표 (핵심 추가)
    # -------------------------

    # 알파벳 (위쪽 + 아래쪽)
    for i in range(size):

        label = chr(ord("A") + i)

        # I 제외 (바둑 표준)
        if label >= "I":
            label = chr(ord("A") + i + 1)

        ax.text(i, -1, label, ha="center", va="center", fontsize=9)
        ax.text(i, size, label, ha="center", va="center", fontsize=9)

    # 숫자 (왼쪽 + 오른쪽)
    for i in range(size):

        num = str(size - i)

        ax.text(-1, i, num, ha="center", va="center", fontsize=9)
        ax.text(size, i, num, ha="center", va="center", fontsize=9)

    # -------------------------
    # 보기 설정
    # -------------------------
    ax.set_xlim(-2, size + 1)
    ax.set_ylim(size, -2)

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_aspect("equal")

    return fig
