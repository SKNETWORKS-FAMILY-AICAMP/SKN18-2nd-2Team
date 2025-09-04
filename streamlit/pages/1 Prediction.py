import streamlit as st
import random

#####################################
# 고객 이탈 확률 예측 페이지 만들기 #
#####################################

# 1. 고객 데이터를 입력하는 폼 만들기
# 2. 랜덤으로 고객 선택
# 3. 이탈 확률을 예측하기
#     - 입력된 고객데이터를 통해 모델 예측 결과를 표시하기
# 4. 고객 정보 및 시각화
#     - 고객 정보와 모델예측 결과를 표시
# 5. 이탈 사유 표시
#     - 예측 결과에 따른 주요 이탈 행동요인을 텍스트 혹은 그래프로 표시

st.title("🔎고객 이탈 확률 예측🔎")
st.write("")
st.write("")
st.subheader("1️⃣ 버튼을 누르면 랜덤으로 고객을 지정합니다.")

# 예시 고객 데이터
customers = [
    {"이름": "홍길동", "나이": 30, "가입기간": 12, "이용횟수": 5},
    {"이름": "김철수", "나이": 25, "가입기간": 6, "이용횟수": 2},
    {"이름": "이영희", "나이": 40, "가입기간": 24, "이용횟수": 10},
]


# 버튼을 누르면 랜덤으로 고객이 지정됨
if st.button("랜덤 고객 뽑기"):
    customer = random.choice(customers)
    st.write("고객 정보:", customer)
    # 예시 확률
    prob = round(random.uniform(0, 1), 2)
    st.metric("이탈 확률", f"{prob*100}%")
    st.bar_chart({"이탈 확률": [prob], "잔존 확률": [1-prob]})
    st.write("이탈 사유 예시: 기프트카드 만료")

st.write("")
st.write("")
st.divider()


# 직접 고객을 선택할 경우
st.subheader("2️⃣ 고객을 직접 입력하여 조회해보세요.")
with st.form("predict_form"):
    age = st.number_input("나이", 18, 100)
    period = st.number_input("가입기간(개월)", 1, 60)
    usage = st.number_input("이용횟수", 0, 100)
    submitted = st.form_submit_button("예측")
    if submitted:
        # 예시 확률
        prob = round(random.uniform(0, 1), 2)
        st.metric("이탈 확률", f"{prob*100}%")
        st.bar_chart({"이탈 확률": [prob], "잔존 확률": [1-prob]})
        st.write("이탈 사유 예시: 구독 기간 만료")


#################
# Side Bar 설정 #
#################

# 기본 sidebar 없애기
st.markdown("""
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# sidebar에 각각의 페이지로 넘어가도록 연결하기
st.sidebar.header("🚀페이지 이동🚀")
st.sidebar.page_link("app.py", label="📍기본 페이지📍")
st.sidebar.page_link("pages/1 Prediction.py", label="🔎고객 이탈 확률 예측🔎")
st.sidebar.page_link("pages/2 Recommendations.py", label="🪄프로모션 추천🪄")
st.sidebar.page_link("pages/3 Reasons.py", label="📊이탈 사유 분석📊")
st.sidebar.success("🙋🏻버튼을 클릭하여 원하는 기능을 사용해보세요!💁🏻‍♀️")