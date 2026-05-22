import sys
import os

sys.path.append(os.path.dirname(__file__))

import matplotlib
matplotlib.use("Agg")

import streamlit as st
import matplotlib.pyplot as plt

from engine.board import GoBoard, BLACK, WHITE
from engine.ai import GoAI
from engine.scoring import score_game
from ui.renderer import render_board


# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="MCTS 바둑 AI",
    layout="wide"
)


# -----------------------------
# 세션 상태 초기화
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

if "last_ai_winrate" not in st.session_state:
    st.session_state.last_ai_winrate = 0.5


board = st.session_state.board
ai = st.session_state.ai


# -----------------------------
# 제목
# -----------------------------
st.title("19x19 한국식 MCTS 바둑 AI")


# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:

    st.header("게임 설정")

    color_choice = st.radio(
        "플레이 색상",
        ["흑", "백"]
    )

    st.session_state.player_color = (
        BLACK if color_choice == "흑" else WHITE
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


# -----------------------------
# 레이아웃
# -----------------------------
left_col, right_col = st.columns([3, 1])


# -----------------------------
# 바둑판 출력
# -----------------------------
with left_col:

    st.subheader("바둑판")

    fig = render_board(board)

    st.pyplot(fig, clear_figure=False)


# -----------------------------
# 우측 정보 패널
# -----------------------------
with right_col:

    current_turn = (
        "흑"
        if board.turn == BLACK
        else "백"
    )

    st.subheader("현재 상태")

    st.write(f"현재 차례: {current_turn}")

    st.write(
        f"흑 사석: {board.black_captures}"
    )

    st.write(
        f"백 사석: {board.white_captures}"
    )

    st.write(
        f"AI 최근 승률: "
        f"{st.session_state.last_ai_winrate:.2%}"
    )

    st.markdown("---")

    st.subheader("착수")

    row = st.number_input(
        "행 (0~18)",
        min_value=0,
        max_value=18,
        value=3,
        step=1
    )

    col = st.number_input(
        "열 (0~18)",
        min_value=0,
        max_value=18,
        value=3,
        step=1
    )

    # -------------------------
    # 플레이어 착수
    # -------------------------
    if st.button("돌 놓기"):

        if st.session_state.game_over:
            st.warning("이미 종료된 게임입니다.")

        else:

            player_color = st.session_state.player_color

            if board.turn != player_color:
                st.warning("현재 AI 차례입니다.")

            else:

                success = board.place_stone(
                    int(row),
                    int(col)
                )

                if not success:
                    st.error("불가능한 수입니다.")

                else:

                    # -----------------
                    # AI 착수
                    # -----------------
                    if not board.game_over():

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

    # -------------------------
    # 패스
    # -------------------------
    if st.button("패스"):

        if not st.session_state.game_over:

            board.pass_turn()

            # 연속 패스면 종료
            if board.game_over():

                black_score, white_score = (
                    score_game(board)
                )

                if black_score > white_score:
                    winner = "흑"
                else:
                    winner = "백"

                st.session_state.winner_text = (
                    f"{winner} 승 "
                    f"(흑 {black_score:.1f}"
                    f" / 백 {white_score:.1f})"
                )

                st.session_state.game_over = True

            else:

                # AI도 패스 가능
                if board.turn != st.session_state.player_color:

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

                    if ai_move is None:
                        board.pass_turn()
                    else:
                        board.place_stone(
                            ai_move[0],
                            ai_move[1]
                        )

            st.rerun()

    # -------------------------
    # 항복
    # -------------------------
    if st.button("항복"):

        if not st.session_state.game_over:

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

    # -------------------------
    # 수동 계가
    # -------------------------
    if st.button("계가"):

        black_score, white_score = (
            score_game(board)
        )

        if black_score > white_score:
            winner = "흑"
        else:
            winner = "백"

        st.session_state.winner_text = (
            f"{winner} 승 "
            f"(흑 {black_score:.1f}"
            f" / 백 {white_score:.1f})"
        )

        st.session_state.game_over = True

        st.rerun()


# -----------------------------
# 승률 그래프
# -----------------------------
st.subheader("AI 승률 그래프")

if len(st.session_state.winrate_history) > 0:

    fig2, ax = plt.subplots(figsize=(10, 3))

    ax.plot(
        st.session_state.winrate_history
    )

    ax.set_ylim(0, 1)

    ax.set_ylabel("AI 승률")

    ax.set_xlabel("턴")

    st.pyplot(fig2, clear_figure=False)

else:

    st.info(
        "아직 승률 데이터가 없습니다."
    )


# -----------------------------
# 종료 표시
# -----------------------------
if st.session_state.game_over:

    st.markdown("---")

    st.success(
        f"게임 종료: "
        f"{st.session_state.winner_text}"
    )
