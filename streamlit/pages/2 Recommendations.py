import streamlit as st
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from utils import load_data

###############################
# 프로모션 추천 페이지 만들기 #
###############################

# 1. 이탈 가능성이 높은 고객 리스트
#     - 이탈 가능성이 높은 고객을 그래프로 보여주기
# 2. 프로모션 추천
#     - 각 고객별로 맞춤형 프로모션을 추천 
#     ex) 할인, 기프트카드 등등

# 기본 sidebar 없애기
st.markdown("""
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

st.title("🪄프로모션 추천🪄")

# 이탈한 고객들만 필터링하고 프로모션 추천 로직 추가
def get_churned_customers_with_promotions():
    _, df = load_data("../data/train.csv","../data/test.csv")
    churned_customers = df[df['churned'] == 1].copy()
    
    # 프로모션 추천 로직
    def recommend_promotion(row):
        if row['payment_method'] == 'Gift Card':
            return "기프트카드 연장 혜택"
        elif row['last_login_days'] > 30:
            return "재접속 할인 쿠폰 (20% 할인)"
        elif row['watch_hours'] < 5:
            return "콘텐츠 추천 + 첫 달 무료"
        elif row['subscription_type'] == 'Basic':
            return "Standard 업그레이드 할인"
        elif row['monthly_fee'] > 15:
            return "Premium 플랜 할인 혜택"
        else:
            return "개인 맞춤 콘텐츠 추천"
    
    # 프로모션 추천 적용
    churned_customers['추천_프로모션'] = churned_customers.apply(recommend_promotion, axis=1)
    
    return churned_customers

customers = get_churned_customers_with_promotions()

# 이탈한 고객들 (실제로 churned=1인 고객들)
st.subheader("👥실제 이탈한 고객 목록")
st.write(f"총 {len(customers)}명의 이탈 고객이 발견되었습니다.")

# 상위 20명의 고객만 표시 (너무 많은 경우)
display_customers = customers.head(20)

# 고객 정보를 더 상세하게 표시
st.dataframe(
    display_customers[[
        'customer_id', 'age', 'gender', 'subscription_type', 
        'watch_hours', 'last_login_days', 'payment_method',
        '추천_프로모션'
    ]].rename(columns={
        'customer_id': '고객ID',
        'age': '나이',
        'gender': '성별', 
        'subscription_type': '구독타입',
        'watch_hours': '월시청시간',
        'last_login_days': '마지막로그인',
        'payment_method': '결제방법',
        '추천_프로모션': '추천프로모션'
    }),
    use_container_width=True
)

# 프로모션 유형별 통계
st.subheader("📊프로모션 유형별 분포")
promotion_counts = customers['추천_프로모션'].value_counts()

# 이탈 고객이므로 빨간색으로 표시
st.markdown("""
<div style="padding: 10px; background-color: #FFE6E6; border-left: 5px solid #FF4B4B; margin: 10px 0;">
    <strong>🔴 이탈 고객 데이터</strong> - 아래 차트는 실제 이탈한 고객들의 분포입니다.
</div>
""", unsafe_allow_html=True)

# 기본 바 차트 사용 (색상 구분을 위한 설명 추가)
st.bar_chart(promotion_counts)

# 세부 분석
col1, col2 = st.columns(2)

with col1:
    st.subheader("💳결제 방법별 이탈 고객")
    payment_counts = customers['payment_method'].value_counts()
    
    # 이탈 고객 데이터임을 표시
    st.markdown("🔴 **이탈 고객 분포**")
    st.bar_chart(payment_counts)

with col2:
    st.subheader("📺구독 타입별 이탈 고객")
    subscription_counts = customers['subscription_type'].value_counts()
    
    # 이탈 고객 데이터임을 표시
    st.markdown("🔴 **이탈 고객 분포**")
    st.bar_chart(subscription_counts)

st.write("**💡 프로모션 추천 전략:**")
st.write("- 기프트카드 사용자: 카드 연장 혜택 제공")
st.write("- 장기 미접속자: 재접속 유도 할인 쿠폰")
st.write("- 저시청자: 맞춤 콘텐츠 추천 및 무료 체험")
st.write("- Basic 사용자: 상위 플랜 업그레이드 할인")


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