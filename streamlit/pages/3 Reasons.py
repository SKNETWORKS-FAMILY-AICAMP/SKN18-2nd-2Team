import streamlit as st
import pandas as pd
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from utils import load_data
from sidebar_utils import setup_shared_sidebar

##################################
# 고객이탈사유 분석페이지 만들기 #
##################################
# 1. 이탈자별 주요 이탈 사유 시각화
#   - 고객별 이탈에 영향을 준 주요 피처를 그래프로 시각화
#   - 이탈 가능성이 높은 이유를 시사하기




st.title("📊이탈 사유 분석📊")
st.write("")
st.write("")

_, df = load_data("../data/train.csv","../data/test.csv")
churned_customers = df[df['churned'] == 1].copy()

# 전체 통계
total_customers = len(df)
churned_count = len(churned_customers)
churn_rate = (churned_count / total_customers) * 100

st.subheader("📈전체 이탈 현황")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("전체 고객 수", f"{total_customers:,}명")
with col2:
    st.metric("이탈 고객 수", f"{churned_count:,}명")
with col3:
    st.metric("이탈률", f"{churn_rate:.1f}%")

# 객관적 데이터 분석으로 대체
st.info("💡 **이탈 사유 분석**: 머신러닝 모델의 Feature Importance나 통계적 분석을 통해 실제 이탈 원인을 파악할 수 있습니다.")

# 고객 특성별 이탈 분석
st.subheader("👥고객 특성별 이탈 분석")

col1, col2 = st.columns(2)

with col1:
    st.write("**결제 방법별 이탈률**")
    payment_churn = df.groupby('payment_method').agg({
        'churned': ['count', 'sum']
    }).round(2)
    payment_churn.columns = ['총고객수', '이탈고객수']
    payment_churn['이탈률(%)'] = (payment_churn['이탈고객수'] / payment_churn['총고객수'] * 100).round(1)
    
    # 이탈률 차트 (이탈률이므로 빨간색 표시)
    st.markdown("🔴 **이탈률 분포**")
    st.bar_chart(payment_churn['이탈률(%)'])
    st.dataframe(payment_churn)

with col2:
    st.write("**구독 타입별 이탈률**")
    subscription_churn = df.groupby('subscription_type').agg({
        'churned': ['count', 'sum']
    }).round(2)
    subscription_churn.columns = ['총고객수', '이탈고객수']
    subscription_churn['이탈률(%)'] = (subscription_churn['이탈고객수'] / subscription_churn['총고객수'] * 100).round(1)
    
    # 이탈률 차트 (이탈률이므로 빨간색 표시)
    st.markdown("🔴 **이탈률 분포**")
    st.bar_chart(subscription_churn['이탈률(%)'])
    st.dataframe(subscription_churn)

# 시청 시간과 이탈의 관계
st.write("")
st.write("")
st.subheader("📺시청 패턴과 이탈의 관계")

# 시청 시간 구간별 이탈률
df['watch_hours_category'] = pd.cut(df['watch_hours'], 
                                   bins=[0, 2, 5, 10, 20, float('inf')], 
                                   labels=['0-2시간', '2-5시간', '5-10시간', '10-20시간', '20시간+'])

watch_category_churn = df.groupby('watch_hours_category').agg({
    'churned': ['count', 'sum']
}).round(2)
watch_category_churn.columns = ['총고객수', '이탈고객수']
watch_category_churn['이탈률(%)'] = (watch_category_churn['이탈고객수'] / watch_category_churn['총고객수'] * 100).round(1)

# 시청 시간별 이탈률 차트 (이탈률이므로 빨간색 표시)
st.markdown("🔴 **시청 패턴별 이탈률**")
st.bar_chart(watch_category_churn['이탈률(%)'])
st.dataframe(watch_category_churn)

# 핵심 인사이트
st.write("")
st.write("")
st.subheader("💡핵심 인사이트")
st.write("**주요 발견사항:**")

# 가장 높은 이탈률을 가진 결제 방법
highest_payment_churn = payment_churn['이탈률(%)'].idxmax()
highest_payment_rate = payment_churn.loc[highest_payment_churn, '이탈률(%)']

st.write(f"- **{highest_payment_churn}** 결제 방법의 이탈률이 **{highest_payment_rate}%**로 가장 높음")

# 가장 높은 이탈률을 가진 구독 타입
highest_sub_churn = subscription_churn['이탈률(%)'].idxmax()
highest_sub_rate = subscription_churn.loc[highest_sub_churn, '이탈률(%)']

st.write(f"- **{highest_sub_churn}** 구독의 이탈률이 **{highest_sub_rate}%**로 가장 높음")

# 데이터 기반 인사이트만 제공

st.write("**데이터 기반 개선 방안:**")
st.write("- 높은 이탈률을 보이는 결제 방법 및 구독 타입에 대한 맞춤형 대응")
st.write("- 시청 패턴 분석을 통한 개인화된 콘텐츠 추천")
st.write("- 고객 세그먼트별 차별화된 리텐션 전략 수립")



setup_shared_sidebar()