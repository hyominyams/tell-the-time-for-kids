import random
import time
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# ---------------------------
# 시계 그리기 함수 (1분 눈금 포함)
# ---------------------------
def draw_clock(hour: int, minute: int):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_aspect("equal")
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.axis("off")

    # 시계 외곽 원
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=3)
    ax.add_patch(circle)

    # --- 분 눈금(틱) 60개 그리기 ---
    for i in range(60):
        angle = np.pi / 2 - np.deg2rad(i * 6)  # 12시가 위, 시계 방향

        # 5분 단위는 더 길고 두껍게
        if i % 5 == 0:
            r_inner = 0.88
            lw = 2
        else:
            r_inner = 0.94
            lw = 1

        r_outer = 1.0
        x1 = r_inner * np.cos(angle)
        y1 = r_inner * np.sin(angle)
        x2 = r_outer * np.cos(angle)
        y2 = r_outer * np.sin(angle)

        ax.plot([x1, x2], [y1, y2], linewidth=lw)

    # 숫자(1~12) 표시
    for h in range(1, 13):
        angle = np.pi / 2 - np.deg2rad((h % 12) * 30)
        x = 0.75 * np.cos(angle)
        y = 0.75 * np.sin(angle)
        ax.text(x, y, str(h), ha="center", va="center", fontsize=14)

    # --- 각도 계산 (분에 따라 시침이 조금씩 움직이게) ---
    # 분침: 1분당 6도
    minute_angle_deg = minute * 6
    # 시침: 1시간당 30도 + 1분당 0.5도
    hour_angle_deg = (hour % 12) * 30 + minute * 0.5

    # 수학 좌표계 기준 각도 (12시가 위, 시계 방향)
    minute_angle = np.pi / 2 - np.deg2rad(minute_angle_deg)
    hour_angle = np.pi / 2 - np.deg2rad(hour_angle_deg)

    # 시침 끝점 (길이 0.5)
    hx = 0.5 * np.cos(hour_angle)
    hy = 0.5 * np.sin(hour_angle)

    # 분침 끝점 (길이 0.75)
    mx = 0.75 * np.cos(minute_angle)
    my = 0.75 * np.sin(minute_angle)

    # 시침
    ax.plot([0, hx], [0, hy], linewidth=5)
    # 분침
    ax.plot([0, mx], [0, my], linewidth=3)
    # 중심점
    ax.plot(0, 0, "o", markersize=8)

    return fig


# ---------------------------
# 새로운 문제 생성
# ---------------------------
def generate_problem(mode: str = "five"):
    # mode:
    # - "hour": 정시만 (예: 3:00)
    # - "half": 30분 단위 (예: 3:00, 3:30)
    # - "five": 5분 단위
    # - "one": 1분 단위
    hour = random.randint(1, 12)

    if mode == "hour":
        minute = 0
    elif mode == "half":
        minute = random.choice([0, 30])
    elif mode == "one":
        minute = random.randint(0, 59)
    else:  # 기본: 5분 단위
        minute = random.choice(list(range(0, 60, 5)))

    return hour, minute


def do_rerun(delay_sec: float = 0.0):
    # delay_sec 동안 잠깐 보여준 뒤 전체 앱을 다시 실행
    if delay_sec > 0:
        time.sleep(delay_sec)

    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


# ---------------------------
# 초기 세션 상태 설정
# ---------------------------
if "mode" not in st.session_state:
    # 초1 기준으로 제일 쉬운 단계(정시 읽기)부터 시작
    st.session_state.mode = "hour"

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
st.title("⏰ 초등 1학년용 시계 읽기 연습")

st.markdown(
    '''
이 앱은 **아날로그 시계 읽기 연습**을 위한 도구입니다.  
난이도를 조절하면서 **시**와 **분**을 읽는 연습을 해 보세요!
'''
)

# 🔹 난이도 4단계 (2단계 추가됨: 정시, 30분)
mode_label = st.radio(
    "난이도 선택",
    (
        "1단계: 정시 읽기 (예: 3시)",
        "2단계: 30분 단위 (예: 3시 30분)",
        "3단계: 5분 단위",
        "4단계: 1분 단위",
    ),
    horizontal=True,
)

if "정시" in mode_label:
    internal_mode = "hour"
elif "30분" in mode_label:
    internal_mode = "half"
elif "5분" in mode_label:
    internal_mode = "five"
else:
    internal_mode = "one"

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
            st.success("🎉 정답입니다! 잘했어요! 다음 문제가 나와요.")
            st.session_state.correct += 1
            st.balloons()

            # ✅ 정답일 때 자동 다음 문제 생성
            h, m = generate_problem(st.session_state.mode)
            st.session_state.problem_hour = h
            st.session_state.problem_minute = m

            # ✅ 1.5초 동안 정답 메시지/빵빠레 보여준 뒤 리렌더
            do_rerun(delay_sec=1.5)
        else:
            st.error(
                f"아쉽네요 😢 정답은 **{correct_hour}시 {correct_minute}분** 이었어요."
            )

    if new_btn:
        h, m = generate_problem(st.session_state.mode)
        st.session_state.problem_hour = h
        st.session_state.problem_minute = m
        do_rerun()

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
