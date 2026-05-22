import sys
import os
import io

import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image

sys.path.append(os.path.dirname(__file__))

from engine.board import GoBoard, BLACK, WHITE
from engine.ai import GoAI
from engine.scoring import score_game
from ui.renderer import render_board


# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="Go AI",
    layout="wide"
)


# -----------------------------
# 초기 세팅
# -----------------------------
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


board = st.session_state.board
ai = st.session_state.ai


# -----------------------------
# 제목
# -----------------------------
st.title("19x19 바둑 AI (A1 입력 버전)")


# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:

    st.header("설정")

    color = st.radio("플레이 색상", ["흑", "백"])

    st.session_state.player_color = (
        BLACK if color == "흑" else WHITE
    )

    if st.button("새 게임"):

        st.session_state.board = GoBoard(19)
        st.session_state.ai = GoAI()
        st.session_state.game_over = False
        st.session_state.winner_text = ""
        st.session_state.winrate_history = []

        st.rerun()


# -----------------------------
# 바둑판 표시
# -----------------------------
st.subheader("바둑판")

fig = render_board(board)

buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight")
buf.seek(0)

image = Image.open(buf)

st.image(image)


# -----------------------------
# 입력 (A1 방식)
# -----------------------------
move = st.text_input("착수 (예: D4, Q16)")

if st.button("착수"):

    if not st.session_state.game_over:

        if move and len(move) >= 2:

            col_char = move[0].upper()
            row_num = move[1:]

            # column 변환 (A-H, J-T)
            col = ord(col_char) - ord("A")
            if col_char >= "I":
                col -= 1

            try:
                row = int(row_num) - 1
                row = 18 - row
            except:
                st.error("형식 오류 (예: D4)")
                st.stop()

            if (
                0 <= row < 19
                and 0 <= col < 19
            ):

                if board.turn == st.session_state.player_color:

                    success = board.place_stone(row, col)

                    if success:

                        with st.spinner("AI 생각 중..."):

                            ai_move, winrate = ai.select_move(board)

                        st.session_state.winrate_history.append(winrate)

                        if ai_move:

                            board.place_stone(
                                ai_move[0],
                                ai_move[1]
                            )

                        st.rerun()

            else:

                st.error("범위를 벗어난 수입니다.")


# -----------------------------
# 패스 / 계가 / 항복
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:

    if st.button("패스"):

        board.pass_turn()

        if board.game_over():

            black, white = score_game(board)

            winner = "흑" if black > white else "백"

            st.session_state.winner_text = (
                f"{winner} 승 (흑 {black:.1f} / 백 {white:.1f})"
            )

            st.session_state.game_over = True

        st.rerun()


with col2:

    if st.button("계가"):

        black, white = score_game(board)

        winner = "흑" if black > white else "백"

        st.session_state.winner_text = (
            f"{winner} 승 (흑 {black:.1f} / 백 {white:.1f})"
        )

        st.session_state.game_over = True

        st.rerun()


with col3:

    if st.button("항복"):

        loser = (
            "흑"
            if st.session_state.player_color == BLACK
            else "백"
        )

        winner = "백" if loser == "흑" else "흑"

        st.session_state.winner_text = f"{loser} 항복 → {winner} 승"

        st.session_state.game_over = True

        st.rerun()


# -----------------------------
# 승률 그래프
# -----------------------------
st.subheader("AI 승률")

if st.session_state.winrate_history:

    fig2, ax = plt.subplots()

    ax.plot(st.session_state.winrate_history)

    ax.set_ylim(0, 1)

    ax.set_xlabel("턴")
    ax.set_ylabel("승률")

    st.pyplot(fig2)

else:

    st.info("아직 데이터 없음")


# -----------------------------
# 종료 표시
# -----------------------------
if st.session_state.game_over:

    st.success(st.session_state.winner_text)
