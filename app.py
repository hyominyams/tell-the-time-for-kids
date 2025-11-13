import random
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# ---------------------------
# 시계 그리기 함수
# ---------------------------
def draw_clock(hour: int, minute: int):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_aspect("equal")
    ax.axis("off")

    # 시계 외곽 원
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=3)
    ax.add_patch(circle)

    # 숫자(1~12) 표시
    for h in range(1, 13):
        angle = np.pi / 6 * (h - 3)  # 12시가 위로 오도록 -3 보정
        x = 0.8 * np.cos(angle)
        y = 0.8 * np.sin(angle)
        ax.text(x, y, str(h), ha="center", va="center", fontsize=14)

    # --- 각도 계산 (분에 따라 시침이 조금씩 움직이게) ---
    # 분침: 1분당 6도
    minute_angle_deg = minute * 6
    # 시침: 1시간당 30도 + 1분당 0.5도
    hour_angle_deg = (hour % 12) * 30 + minute * 0.5

    # 라디안으로 변환 (위쪽이 12시가 되도록 -90도 보정: -pi/2)
    minute_angle = np.deg2rad(minute_angle_deg) - np.pi / 2
    hour_angle = np.deg2rad(hour_angle_deg) - np.pi / 2

    # 시침 끝점 (길이 0.5)
    hx = 0.5 * np.cos(hour_angle)
    hy = 0.5 * np.sin(hour_angle)

    # 분침 끝점 (길이 0.75)
    mx = 0.75 * np.cos(minute_angle)
    my = 0.75 * np.sin(minute_angle)

    # 시침
    ax.plot([0, hx], [0, hy], linewidth=6)
    # 분침
    ax.plot([0, mx], [0, my], linewidth=3)
    # 중심점
    ax.plot(0, 0, "o", markersize=8)

    return fig


# ---------------------------
# 새로운 문제 생성
# ---------------------------
def generate_problem(mode: str = "easy"):
    # 쉬움: 5분 단위 / 보통: 1분 단위
    hour = random.randint(1, 12)
    if mode == "easy":
        minute = random.choice(list(range(0, 60, 5)))
    else:
        minute = random.randint(0, 59)
    return hour, minute


# ---------------------------
# 초기 세션 상태 설정
# ---------------------------
if "mode" not in st.session_state:
    st.session_state.mode = "easy"

if "problem_hour" not in st.session_state or "problem_minute" not in st.session_state:
    h, m = generate_problem(st.session_state.mode)
    st.session_state.problem_hour = h
    st.session_state.problem_minute = m

if "total" not in st.session_state:
    st.session_state.total = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0


# ---------------------------
# UI 구성
# ---------------------------
st.title("⏰ 초등 저학년용 시계 읽기 연습")

st.markdown(
    """
이 앱은 **아날로그 시계 읽기 연습**을 위한 도구입니다.  
시계를 보고 **시**와 **분**을 맞게 적어 보세요!
"""
)

# 난이도 선택
mode = st.radio(
    "난이도 선택",
    (
        "쉬움 (5분 단위)",
        "보통 (1분 단위)",
    ),
    horizontal=True,
)

# 내부에서 사용할 모드 문자열
internal_mode = "easy" if "쉬움" in mode else "normal"
st.session_state.mode = internal_mode

col1, col2 = st.columns(2)

with col1:
    st.subheader("문제 시계")
    fig = draw_clock(st.session_state.problem_hour, st.session_state.problem_minute)
    st.pyplot(fig)

with col2:
    st.subheader("현재 시각은 몇 시 몇 분일까요?")

    user_hour = st.number_input("시 (1~12)", min_value=1, max_value=12, step=1, value=1)
    user_minute = st.number_input(
        "분 (0~59)", min_value=0, max_value=59, step=1, value=0
    )

    check_btn = st.button("정답 확인")
    new_btn = st.button("새 문제 만들기")

    if check_btn:
        st.session_state.total += 1

        correct_hour = st.session_state.problem_hour
        correct_minute = st.session_state.problem_minute

        if (user_hour == correct_hour) and (user_minute == correct_minute):
            st.success("🎉 정답입니다! 잘했어요!")
            st.session_state.correct += 1
            st.balloons()
        else:
            st.error(
                f"아쉽어요 😢 정답은 **{correct_hour}시 {correct_minute}분** 이었어요."
            )

    if new_btn:
        h, m = generate_problem(st.session_state.mode)
        st.session_state.problem_hour = h
        st.session_state.problem_minute = m
        st.experimental_rerun()

# ---------------------------
# 점수/통계
# ---------------------------
st.markdown("---")
st.subheader("내 기록")

if st.session_state.total > 0:
    rate = st.session_state.correct / st.session_state.total * 100
    st.write(f"🔢 총 문제 수: **{st.session_state.total}**")
    st.write(f"✅ 맞힌 개수: **{st.session_state.correct}**")
    st.write(f"📊 정답률: **{rate:.1f}%**")
else:
    st.write("아직 푼 문제가 없어요. 문제를 풀어 보세요!")
