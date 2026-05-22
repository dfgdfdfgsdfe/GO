import matplotlib
matplotlib.use("Agg")

import io

import streamlit as st
import matplotlib.pyplot as plt

from PIL import Image

from streamlit_image_coordinates import (
    streamlit_image_coordinates
)

from engine.board import (
    GoBoard,
    BLACK,
    WHITE
)

from engine.ai import GoAI

from engine.scoring import score_game

from ui.renderer import render_board


# ---------------------------------
# 페이지 설정
# ---------------------------------
st.set_page_config(
    page_title="MCTS 바둑 AI",
    layout="wide"
)


# ---------------------------------
# 세션 상태 초기화
# ---------------------------------
if "board" not in st.session_state:

    st.session_state.board = GoBoard(19)

if "ai" not in st.session_state:

    st.session_state.ai = GoAI()

if "player_color" not in st.session_state:

    st.session_state.player_color = BLACK

if "game_over" not in st.session_state:

    st.session_state.game_over = False

if "winner_text" not in st.session_state:

    st.session_state.winner_text = ""

if "winrate_history" not in st.session_state:

    st.session_state.winrate_history = []

if "last_ai_winrate" not in st.session_state:

    st.session_state.last_ai_winrate = 0.5


board = st.session_state.board
ai = st.session_state.ai


# ---------------------------------
# 제목
# ---------------------------------
st.title("19x19 한국식 MCTS 바둑 AI")


# ---------------------------------
# 사이드바
# ---------------------------------
with st.sidebar:

    st.header("설정")

    side = st.radio(
        "플레이 색상",
        ["흑", "백"]
    )

    st.session_state.player_color = (
        BLACK if side == "흑"
        else WHITE
    )

    st.markdown("---")

    if st.button("새 게임"):

        st.session_state.board = GoBoard(19)

        st.session_state.ai = GoAI()

        st.session_state.game_over = False

        st.session_state.winner_text = ""

        st.session_state.winrate_history = []

        st.session_state.last_ai_winrate = 0.5

        st.rerun()


# ---------------------------------
# 레이아웃
# ---------------------------------
left_col, right_col = st.columns([3, 1])


# ---------------------------------
# 바둑판 표시
# ---------------------------------
with left_col:

    st.subheader("바둑판")

    fig = render_board(board)

    buf = io.BytesIO()

    fig.savefig(
        buf,
        format="png",
        bbox_inches="tight"
    )

    buf.seek(0)

    image = Image.open(buf)

    clicked = (
        streamlit_image_coordinates(
            image,
            key="board"
        )
    )

    # -----------------------------
    # 클릭 착수
    # -----------------------------
    if (
        clicked is not None
        and
        not st.session_state.game_over
    ):

        px = clicked["x"]
        py = clicked["y"]

        width, height = image.size

        board_x = round(
            py / (height / 19)
        )

        board_y = round(
            px / (width / 19)
        )

        board_x = max(
            0,
            min(18, board_x)
        )

        board_y = max(
            0,
            min(18, board_y)
        )

        if (
            board.turn
            ==
            st.session_state.player_color
        ):

            success = board.place_stone(
                board_x,
                board_y
            )

            if success:

                with st.spinner(
                    "AI가 생각 중..."
                ):

                    ai_move, winrate = (
                        ai.select_move(board)
                    )

                st.session_state.last_ai_winrate = (
                    winrate
                )

                st.session_state.winrate_history.append(
                    winrate
                )

                if ai_move is not None:

                    board.place_stone(
                        ai_move[0],
                        ai_move[1]
                    )

                st.rerun()


# ---------------------------------
# 우측 패널
# ---------------------------------
with right_col:

    current_turn = (
        "흑"
        if board.turn == BLACK
        else "백"
    )

    st.subheader("현재 상태")

    st.write(
        f"현재 차례: {current_turn}"
    )

    st.write(
        f"흑 사석: "
        f"{board.black_captures}"
    )

    st.write(
        f"백 사석: "
        f"{board.white_captures}"
    )

    st.write(
        f"AI 최근 승률: "
        f"{st.session_state.last_ai_winrate:.1%}"
    )

    st.markdown("---")

    # -----------------------------
    # 패스
    # -----------------------------
    if st.button("패스"):

        board.pass_turn()

        if board.game_over():

            black, white = (
                score_game(board)
            )

            winner = (
                "흑"
                if black > white
                else "백"
            )

            st.session_state.winner_text = (
                f"{winner} 승 "
                f"(흑 {black:.1f}"
                f" / 백 {white:.1f})"
            )

            st.session_state.game_over = True

        st.rerun()

    # -----------------------------
    # 계가
    # -----------------------------
    if st.button("계가"):

        black, white = (
            score_game(board)
        )

        winner = (
            "흑"
            if black > white
            else "백"
        )

        st.session_state.winner_text = (
            f"{winner} 승 "
            f"(흑 {black:.1f}"
            f" / 백 {white:.1f})"
        )

        st.session_state.game_over = True

        st.rerun()

    # -----------------------------
    # 항복
    # -----------------------------
    if st.button("항복"):

        loser = (
            "흑"
            if st.session_state.player_color == BLACK
            else "백"
        )

        winner = (
            "백"
            if loser == "흑"
            else "흑"
        )

        st.session_state.winner_text = (
            f"{loser} 항복 → {winner} 승"
        )

        st.session_state.game_over = True

        st.rerun()


# ---------------------------------
# 승률 그래프
# ---------------------------------
st.subheader("AI 승률 그래프")

if st.session_state.winrate_history:

    fig2, ax = plt.subplots(
        figsize=(10, 3)
    )

    ax.plot(
        st.session_state.winrate_history
    )

    ax.set_ylim(0, 1)

    ax.set_ylabel("AI 승률")

    ax.set_xlabel("턴")

    st.pyplot(fig2)

else:

    st.info(
        "아직 승률 데이터가 없습니다."
    )


# ---------------------------------
# 게임 종료 표시
# ---------------------------------
if st.session_state.game_over:

    st.success(
        f"게임 종료: "
        f"{st.session_state.winner_text}"
    )
