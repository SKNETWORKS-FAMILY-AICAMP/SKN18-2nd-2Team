import streamlit as st
import pandas as pd

##################################
# 고객이탈사유 분석페이지 만들기 #
##################################
# 1. 이탈자별 주요 이탈 사유 시각화
#   - 고객별 이탈에 영향을 준 주요 피처를 그래프로 시각화
#   - 이탈 가능성이 높은 이유를 시사하기



st.title("📊이탈 사유 분석📊")


customers = pd.DataFrame([
    {"이름": "홍길동", "주요 이탈 사유": "기프트카드 만료", "영향도": 0.7},
    {"이름": "김철수", "주요 이탈 사유": "이용횟수 감소", "영향도": 0.6},
    {"이름": "이영희", "주요 이탈 사유": "만족도 높음", "영향도": 0.1},
])

st.subheader("📜고객별 이탈 사유")
st.dataframe(customers[["이름", "주요 이탈 사유", "영향도"]])

st.subheader("📈이탈 사유별 영향도 시각화")
st.bar_chart(customers.set_index("이름")["영향도"])


#################
# Side Bar 설정 #
#################
# 각각의 페이지로 넘어가도록 연결하기
st.sidebar.header("🚀페이지 이동🚀")
st.sidebar.page_link("app.py", label="📍기본 페이지📍")
st.sidebar.page_link("pages/1 Prediction.py", label="🔎고객 이탈 확률 예측🔎")
st.sidebar.page_link("pages/2 Recommendations.py", label="🪄프로모션 추천🪄")
st.sidebar.page_link("pages/3 Reasons.py", label="📊이탈 사유 분석📊")
st.sidebar.success("🙋🏻버튼을 클릭하여 원하는 기능을 사용해보세요!💁🏻‍♀️")