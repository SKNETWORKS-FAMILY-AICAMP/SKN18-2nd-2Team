import streamlit as st
import pandas as pd
import numpy as np

###############################
# 프로모션 추천 페이지 만들기 #
###############################

# 1. 이탈 가능성이 높은 고객 리스트
#     - 이탈 가능성이 높은 고객을 그래프로 보여주기
# 2. 프로모션 추천
#     - 각 고객별로 맞춤형 프로모션을 추천 
#     ex) 할인, 기프트카드 등등



st.title("🪄프로모션 추천🪄")

# Netflix 고객 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('data/netflix_customer_churn.csv')

# 이탈한 고객들만 필터링하고 프로모션 추천 로직 추가
def get_churned_customers_with_promotions():
    df = load_data()
    churned_customers = df[df['churned'] == 1].copy()
    
    # 업그레이드된 프로모션 추천 로직
    def recommend_promotion(row):
        # 1. 환영 복귀 할인 (Welcome Back Discount)
        # 조건: Basic 구독 OR Crypto/Gift Card 결제
        if (row['subscription_type'] == 'Basic') or (row['payment_method'] in ['Crypto', 'Gift Card']):
            if row['payment_method'] == 'Gift Card':
                return "🎁 복귀 첫 달 50% 할인 + 기프트카드 연장 혜택"
            elif row['payment_method'] == 'Crypto':
                return "💰 3개월 결제 시 1개월 무료 (암호화폐 결제 혜택)"
            else:  # Basic 구독
                return "🔄 복귀 첫 달 50% 할인 (Basic → Standard 업그레이드 포함)"
        
        # 2. 콘텐츠 기반 복귀 (Don't Miss Out / Sequel Teaser)
        # 조건: 시청시간 < 10시간 AND 특정 장르
        elif row['watch_hours'] < 10:
            if row['favorite_genre'] == 'Drama':
                return "🎬 시즌2 공개 알림! 복귀 시 7일 무료 체험 (드라마 특화)"
            elif row['favorite_genre'] == 'Action':
                return "💥 액션 블록버스터 신작 5편 + 첫 달 30% 할인"
            elif row['favorite_genre'] == 'Comedy':
                return "😂 코미디 추천작 패키지 + 복귀 시 2주 무료"
            elif row['favorite_genre'] == 'Horror':
                return "😱 공포 시리즈 완결편 공개! 7일 무료 체험"
            elif row['favorite_genre'] == 'Sci-Fi':
                return "🚀 SF 대작 시리즈 + 첫 달 30% 할인"
            elif row['favorite_genre'] == 'Romance':
                return "💕 로맨스 신작 라인업 + 복귀 시 10일 무료"
            else:  # Documentary 등
                return "📚 다큐멘터리 특선 + 교육 콘텐츠 무료 체험"
        
        # 3. 현지화 콘텐츠 캠페인 (Localized Win-Back)
        # 조건: 지역별 + 장르별 맞춤
        elif row['region'] in ['Asia', 'South America'] and row['favorite_genre'] == 'Drama':
            if row['region'] == 'Asia':
                return "🌏 K-드라마 열풍! 화제작 시청 + 복귀 시 1주 무료"
            else:  # South America
                return "🌎 라틴 드라마 신작 + 현지화 자막 서비스 무료"
        
        # 4. 장기 미접속자 특별 복귀 캠페인
        elif row['last_login_days'] > 60:
            return "⏰ 장기 미접속자 특별 혜택: 첫 달 70% 할인 + 개인 맞춤 추천"
        elif row['last_login_days'] > 30:
            return "📅 한 달 만에 돌아오신 고객님께: 재접속 30% 할인 쿠폰"
        
        # 5. 프리미엄 고객 맞춤 복귀
        elif row['subscription_type'] == 'Premium' or row['monthly_fee'] > 15:
            return "👑 프리미엄 고객 전용: 4K 콘텐츠 무제한 + 복귀 시 첫 달 무료"
        
        # 6. 디바이스별 맞춤 프로모션
        elif row['device'] == 'Mobile':
            return "📱 모바일 전용: 오프라인 다운로드 무제한 + 첫 달 40% 할인"
        elif row['device'] == 'Smart TV':
            return "📺 스마트 TV 최적화: 4K HDR 콘텐츠 + 가족 계정 무료 추가"
        
        # 7. 가족/다중 프로필 유저 복귀
        elif row['number_of_profiles'] >= 3:
            return "👨‍👩‍👧‍👦 가족 계정 특별 혜택: 프로필 무제한 + 키즈 콘텐츠 무료"
        
        # 8. 기본 복귀 프로모션
        else:
            return "🎯 개인 맞춤 복귀 혜택: AI 추천 콘텐츠 + 첫 달 25% 할인"
    
    # 프로모션 추천 적용
    churned_customers['추천_프로모션'] = churned_customers.apply(recommend_promotion, axis=1)
    
    return churned_customers

customers = get_churned_customers_with_promotions()

# 이탈한 고객들 (실제로 churned=1인 고객들)
st.subheader("👥실제 이탈한 고객 목록")
st.write(f"총 {len(customers)}명의 이탈 고객이 발견되었습니다.")

# 페이지네이션 설정
items_per_page = st.selectbox("페이지당 표시 개수", [20, 50, 100, 200], index=0)
total_pages = (len(customers) - 1) // items_per_page + 1

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    current_page = st.selectbox(
        f"페이지 선택 (총 {total_pages}페이지)",
        range(1, total_pages + 1),
        key="customer_page"
    )

# 현재 페이지의 고객 데이터
start_idx = (current_page - 1) * items_per_page
end_idx = min(start_idx + items_per_page, len(customers))
display_customers = customers.iloc[start_idx:end_idx]

st.info(f"📄 {current_page}페이지: {start_idx + 1}-{end_idx}번째 고객 ({len(display_customers)}명)")

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

# 이탈 고객이므로 빨간색으로 표시
st.markdown("""
<div style="padding: 10px; background-color: #FFE6E6; border-left: 5px solid #FF4B4B; margin: 10px 0;">
    <strong>🔴 이탈 고객 데이터</strong> - 아래 차트는 실제 이탈한 고객들의 분포입니다.
</div>
""", unsafe_allow_html=True)

# 프로모션별 상세 통계
st.markdown("### 📊 프로모션별 상세 통계")
promotion_counts = customers['추천_프로모션'].value_counts()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("총 프로모션 유형", len(promotion_counts))
with col2:
    st.metric("가장 많은 프로모션", promotion_counts.index[0])
with col3:
    st.metric("해당 고객 수", f"{promotion_counts.iloc[0]}명")

# 프로모션별 비율 표시
promotion_df = pd.DataFrame({
    '프로모션 유형': promotion_counts.index,
    '고객 수': promotion_counts.values,
    '비율(%)': (promotion_counts.values / promotion_counts.sum() * 100).round(1)
})

st.markdown("#### 📋 프로모션 유형별 세부 현황")
st.dataframe(promotion_df, use_container_width=True)

# 💡 업그레이드된 프로모션 추천 전략
st.markdown("---")
st.markdown("## 💡 업그레이드된 프로모션 추천 전략")

col_strategy1, col_strategy2 = st.columns(2)

with col_strategy1:
    st.markdown("### 🎯 **핵심 전략**")
    
    st.markdown("#### **1. 환영 복귀 할인 (Welcome Back)**")
    st.markdown("• **대상**: Basic 구독자, Crypto/Gift Card 결제자")
    st.markdown("• **혜택**: 첫 달 50% 할인 + 업그레이드 포함")
    
    st.markdown("#### **2. 콘텐츠 기반 복귀 (Sequel Teaser)**")
    st.markdown("• **대상**: 저시청자 (10시간 미만)")
    st.markdown("• **혜택**: 장르별 맞춤 신작 + 무료 체험")
    
    st.markdown("#### **3. 현지화 콘텐츠 캠페인**")
    st.markdown("• **대상**: 아시아/남미 드라마 선호자")
    st.markdown("• **혜택**: K-드라마, 라틴 드라마 특화 서비스")
    
    st.markdown("#### **4. 장기 미접속자 특별 복귀**")
    st.markdown("• **대상**: 30일/60일 이상 미접속")
    st.markdown("• **혜택**: 최대 70% 할인 + 개인 맞춤 추천")

with col_strategy2:
    st.markdown("### 🚀 **세분화 전략**")
    
    st.markdown("#### **5. 프리미엄 고객 맞춤**")
    st.markdown("• **대상**: Premium 구독자, 고액 결제자")
    st.markdown("• **혜택**: 4K 콘텐츠 무제한 + 첫 달 무료")
    
    st.markdown("#### **6. 디바이스별 맞춤**")
    st.markdown("• **모바일**: 오프라인 다운로드 무제한")
    st.markdown("• **스마트 TV**: 4K HDR + 가족 계정 추가")
    
    st.markdown("#### **7. 가족 계정 특별 혜택**")
    st.markdown("• **대상**: 3개 이상 프로필 사용자")
    st.markdown("• **혜택**: 프로필 무제한 + 키즈 콘텐츠")
    
    st.markdown("#### **8. AI 개인화 추천**")
    st.markdown("• **대상**: 기타 모든 이탈 고객")
    st.markdown("• **혜택**: AI 맞춤 추천 + 25% 할인")

# 핵심 인사이트
st.markdown("#### 💡 핵심 인사이트")
col7, col8, col9 = st.columns(3)

with col7:
    most_common_promo = customers['추천_프로모션'].mode()[0]
    st.metric("가장 필요한 프로모션", most_common_promo)

with col8:
    avg_watch_hours = customers['watch_hours'].mean()
    st.metric("평균 시청시간", f"{avg_watch_hours:.1f}시간")

with col9:
    avg_last_login = customers['last_login_days'].mean()
    st.metric("평균 마지막 로그인", f"{avg_last_login:.1f}일 전")

# 연령대 설정
customers['age_group'] = pd.cut(customers['age'], 
                               bins=[0, 25, 35, 45, 55, 100], 
                               labels=['25세 미만', '25-34세', '35-44세', '45-54세', '55세 이상'])

# 시청 시간대별 분포
watch_bins = pd.cut(customers['watch_hours'], 
                   bins=[0, 5, 10, 20, 50], 
                   labels=['5시간 미만', '5-10시간', '10-20시간', '20시간 이상'])

# 로그인 분포
login_bins = pd.cut(customers['last_login_days'], 
                   bins=[0, 7, 14, 30, 365], 
                   labels=['1주일 이내', '1-2주', '2주-1달', '1달 이상'])

# 📊 그래프 모음 섹션
st.markdown("---")
st.subheader("📊 데이터 시각화 대시보드")

# 첫 번째 행: 프로모션과 결제방법
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 추천 프로모션 유형별 분포")
    # 프로모션 차트 (빨간색 계열)
    promotion_chart_data = pd.DataFrame({
        '프로모션별 고객수': promotion_counts.values
    }, index=promotion_counts.index)
    st.bar_chart(promotion_chart_data, color='#FF6B6B')

with col2:
    st.markdown("#### 💳 결제 방법별 이탈 고객")
    payment_counts = customers['payment_method'].value_counts()
    # 결제방법 차트 (초록색 계열)
    payment_chart_data = pd.DataFrame({
        '결제방법별 고객수': payment_counts.values
    }, index=payment_counts.index)
    st.bar_chart(payment_chart_data, color='#4ECDC4')

# 두 번째 행: 구독타입과 지역
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 📺 구독 타입별 이탈 고객")
    subscription_counts = customers['subscription_type'].value_counts()
    # 구독타입 차트 (보라색 계열)
    subscription_chart_data = pd.DataFrame({
        '구독타입별 고객수': subscription_counts.values
    }, index=subscription_counts.index)
    st.bar_chart(subscription_chart_data, color='#9B59B6')

with col4:
    st.markdown("#### 🌍 지역별 이탈 고객")
    region_counts = customers['region'].value_counts()
    # 지역 차트 (주황색 계열)
    region_chart_data = pd.DataFrame({
        '지역별 고객수': region_counts.values
    }, index=region_counts.index)
    st.bar_chart(region_chart_data, color='#FF9500')

# 세 번째 행: 디바이스와 연령대
col5, col6 = st.columns(2)

with col5:
    st.markdown("#### 📱 디바이스별 이탈 고객")
    device_counts = customers['device'].value_counts()
    # 디바이스 차트 (파란색 계열)
    device_chart_data = pd.DataFrame({
        '디바이스별 고객수': device_counts.values
    }, index=device_counts.index)
    st.bar_chart(device_chart_data, color='#3498DB')

with col6:
    st.markdown("#### 👥 연령대별 이탈 분석")
    age_counts = customers['age_group'].value_counts()
    # 연령대 차트 (핑크색 계열)
    age_chart_data = pd.DataFrame({
        '연령대별 고객수': age_counts.values
    }, index=age_counts.index)
    st.bar_chart(age_chart_data, color='#E91E63')

# 네 번째 행: 시청패턴
col7, col8 = st.columns(2)

with col7:
    st.markdown("#### 📺 월 시청시간 분포")
    watch_distribution = watch_bins.value_counts()
    # 시청시간 차트 (청록색 계열)
    watch_chart_data = pd.DataFrame({
        '시청시간별 고객수': watch_distribution.values
    }, index=watch_distribution.index)
    st.bar_chart(watch_chart_data, color='#1ABC9C')

with col8:
    st.markdown("#### 📅 마지막 로그인 분포")
    login_distribution = login_bins.value_counts()
    # 로그인 차트 (갈색 계열)
    login_chart_data = pd.DataFrame({
        '로그인별 고객수': login_distribution.values
    }, index=login_distribution.index)
    st.bar_chart(login_chart_data, color='#8B4513')

# 다섯 번째 행: 교차 분석
st.markdown("#### 🔥 구독타입별 결제방법 분석")
crosstab_data = pd.crosstab(customers['subscription_type'], customers['payment_method'], margins=True)
st.dataframe(crosstab_data, use_container_width=True)

# 연령대별 상세 분석 테이블
st.markdown("#### 📊 연령대별 상세 분석")
age_analysis = customers.groupby('age_group').agg({
    'watch_hours': 'mean',
    'last_login_days': 'mean',
    'monthly_fee': 'mean'
}).round(2)

age_analysis.columns = ['평균 시청시간', '평균 마지막로그인', '평균 월구독료']
st.dataframe(age_analysis, use_container_width=True)

# 상세 분석 정보
st.markdown("---")
st.markdown("### 🔍 상세 분석 정보")

col_detail1, col_detail2 = st.columns(2)

with col_detail1:
    st.markdown("**💳 결제 방법별 상세 분석:**")
    for method, count in payment_counts.items():
        percentage = (count / len(customers) * 100)
        st.write(f"• {method}: {count}명 ({percentage:.1f}%)")
    
    st.markdown("**🌍 지역별 인사이트:**")
    top_region = region_counts.index[0]
    top_count = region_counts.iloc[0]
    st.info(f"**{top_region}** 지역에서 가장 많은 이탈 발생 ({top_count}명)")

with col_detail2:
    st.markdown("**📺 구독 타입별 상세 분석:**")
    for sub_type, count in subscription_counts.items():
        percentage = (count / len(customers) * 100)
        st.write(f"• {sub_type}: {count}명 ({percentage:.1f}%)")
    
    st.markdown("**📱 디바이스별 인사이트:**")
    top_device = device_counts.index[0]
    top_device_count = device_counts.iloc[0]
    st.info(f"**{top_device}** 사용자의 이탈률이 가장 높음 ({top_device_count}명)")



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