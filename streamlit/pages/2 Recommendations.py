import streamlit as st
import pandas as pd

###############################
# 프로모션 추천 페이지 만들기 #
###############################

# 1. 이탈 가능성이 높은 고객 리스트
#     - 이탈 가능성이 높은 고객을 그래프로 보여주기
# 2. 프로모션 추천
#     - 각 고객별로 맞춤형 프로모션을 추천 
#     ex) 할인, 기프트카드 등등



st.title("🪄프로모션 추천🪄")

# 예시: 실제 데이터 파일이 있다면 아래처럼 불러올 수 있습니다.
# customers = pd.read_csv("data/customers.csv")
customers = pd.DataFrame([
    {"이름": "홍길동", "이탈확률": 0.85, "추천 프로모션": "10% 할인"},
    {"이름": "김철수", "이탈확률": 0.45, "추천 프로모션": "기프트카드 증정"},
    {"이름": "이영희", "이탈확률": 0.15, "추천 프로모션": "-"},
])

high_risk = customers[customers["이탈확률"] > 0.5]
st.subheader("👥이탈 가능성 높은 고객 목록")
st.dataframe(high_risk[["이름", "이탈확률", "추천 프로모션"]])

st.write("고객별 맞춤 프로모션을 추천합니다.")


#################
# Side Bar 설정 #
#################
# sicebar에 각각의 페이지로 넘어가도록 연결하기
st.sidebar.header("🚀페이지 이동🚀")
st.sidebar.page_link("app.py", label="📍기본 페이지📍")
st.sidebar.page_link("pages/1 Prediction.py", label="🔎고객 이탈 확률 예측🔎")
st.sidebar.page_link("pages/2 Recommendations.py", label="🪄프로모션 추천🪄")
st.sidebar.page_link("pages/3 Reasons.py", label="📊이탈 사유 분석📊")
st.sidebar.success("🙋🏻버튼을 클릭하여 원하는 기능을 사용해보세요!💁🏻‍♀️")