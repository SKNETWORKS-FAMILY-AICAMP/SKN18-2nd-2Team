import streamlit as st
import pandas as pd
import math
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
    
    # 업그레이드된 프로모션 추천 로직 (이탈 고객 대상)
    def recommend_promotion(row):
        # 1. 연령별 이탈 방지
        # 대상: 20~30대 그리고 40대 중반에서 60대초반
        if (20 <= row['age'] <= 35) or (45 <= row['age'] <= 65):
            return "🎂 연령대별 특별 할인 30% + 1달 무료체험"
        
        # 2. 월 시청시간 저조자 이탈 방지
        # 대상: 월 시청시간 5시간 미만인자
        elif row['watch_hours'] < 5:
            return "📺 무료 AI 맞춤 추천 + 알림 시스템 + 1달 무료체험"
        
        # 3. 장기 미접속자 복귀 유인
        # 대상: 30일 이상 미접속자
        elif row['last_login_days'] >= 30:
            return "⏰ 복귀 시 최대 70% 할인 + 무료 AI 맞춤 알림 + 1달 무료체험"
        
        # 4. 결제 방법 불편 해소
        # 대상: Gift Card와 Crypto 결제자
        elif row['payment_method'] in ['Gift Card', 'Crypto']:
            if row['payment_method'] == 'Gift Card':
                return "🎁 기프트카드 연속 결제 시 최대 50% 할인"
            else:  # Crypto
                return "💰 암호화폐 연속 결제 시 최대 50% 할인"
        
        # 5. 프리미엄 고객 집중 강화
        # 대상: premium 구독자 및 고액결제자
        elif row['subscription_type'] == 'Premium' or row['monthly_fee'] > 15:
            return "👑 프리미엄 고객 전용: 4K 콘텐츠 무제한 + 첫 달 무료"
        
        # 6. 디바이스별 맞춤 전략
        # 대상: 모바일과 태블릿
        elif row['device'] in ['Mobile', 'Tablet']:
            return "📱 모바일/태블릿 전용: 오프라인 다운로드 무제한"
        
        # 7. 다계정자 특별 강화
        # 대상: 3개 이상 프로필 사용자
        elif row['number_of_profiles'] >= 3:
            return "👨‍👩‍👧‍👦 다계정 특별 혜택: 프로필 무제한 + 키즈 콘텐츠 무료"
        
        # 8. 기본 복귀 프로모션 (기타 이탈 고객)
        else:
            return "🎯 기본 복귀 혜택: AI 개인화 추천 + 25% 할인"
    
    # 프로모션 추천 적용
    churned_customers['추천_프로모션'] = churned_customers.apply(recommend_promotion, axis=1)
    
    return churned_customers


# 전체 고객 데이터 로드 및 프로모션 적용
def get_all_customers_with_promotions():
    df = load_data()
    all_customers = df.copy()
    
    # 이탈 고객과 비이탈 고객에 따라 다른 프로모션 적용
    def recommend_promotion_all(row):
        if row['churned'] == 1:  # 이탈 고객
            # 이탈 고객 전용 프로모션 로직 (1-4번만)
            if (20 <= row['age'] <= 30) or (45 <= row['age'] <= 60):
                return "🔴 연령대별 특별 할인 30% + 1달 무료체험"
            elif row['watch_hours'] < 5:
                return "🔴 무료 AI 맞춤 추천 + 알림 시스템 + 1달 무료체험"
            elif row['last_login_days'] >= 30: 
                return "🔴 복귀 시 최대 70% 할인 + 무료 AI 맞춤 알림 + 1달 무료체험"
            elif row['payment_method'] in ['Gift Card', 'Crypto']:
                return "🔴 기프트카드/암호화폐 연속 결제 시 최대 50% 할인"
        else:  # 비이탈 고객 (churned == 0)
            # 유지 고객 대상 프로모션 로직
            if row['subscription_type'] == 'Premium' or row['monthly_fee'] > 15:
                return "🟢 프리미엄 고객 전용: 4K 콘텐츠 무제한 + 첫 달 무료"
            elif row['device'] in ['Mobile', 'Tablet']:
                return "🟢 모바일/태블릿 전용: 오프라인 다운로드 무제한"
            elif row['number_of_profiles'] >= 3:
                return "🟢 다계정 특별 혜택: 프로필 무제한 + 키즈 콘텐츠 무료"
            else:
                return "🟢 기본 유지 강화: AI 개인화 추천 + 25% 할인"
    
    # 프로모션 추천 적용
    all_customers['추천_프로모션'] = all_customers.apply(recommend_promotion_all, axis=1)
    
    return all_customers

customers = get_all_customers_with_promotions()

# 💡 업그레이드된 프로모션 추천 전략
st.markdown("---")
st.markdown("## 💡 업그레이드된 프로모션 추천 전략")

col_strategy1, col_strategy2 = st.columns(2)

with col_strategy1:
    st.markdown("### 🎯 **이탈 고객 대상 전략 (churn=1)**")
    
    st.markdown("#### **1. 연령별 이탈 방지**")
    st.markdown("• **대상**: 20~30대, 40대 중반~60대 초반 (이탈 고객)")
    st.markdown("• **혜택**: 연령대별 특별 할인 30% + 1달 무료체험")
    
    st.markdown("#### **2. 월 시청시간 저조자 이탈 방지**")
    st.markdown("• **대상**: 월 시청시간 5시간 미만 (이탈 고객)")
    st.markdown("• **혜택**: 무료 AI 맞춤 추천 + 알림 시스템 + 1달 무료체험")
    
    st.markdown("#### **3. 장기 미접속자 복귀 유인**")
    st.markdown("• **대상**: 30일 이상 미접속자 (이탈 고객)")
    st.markdown("• **혜택**: 복귀 시 최대 70% 할인 + 무료 AI 맞춤 알림 + 1달 무료체험")
    
    st.markdown("#### **4. 결제 방법 불편 해소**")
    st.markdown("• **대상**: Gift Card와 Crypto 결제자 (이탈 고객)")
    st.markdown("• **혜택**: 동일 방법 연속 결제 시 최대 50% 할인")

with col_strategy2:
    st.markdown("### 🚀 **유지 대상 고객 전략 (churn=0)**")
    
    st.markdown("#### **5. 프리미엄 고객 집중 강화**")
    st.markdown("• **대상**: Premium 구독자 및 고액결제자 (유지 고객)")
    st.markdown("• **혜택**: 4K 콘텐츠 무제한 + 첫 달 무료")
    
    st.markdown("#### **6. 디바이스별 맞춤 전략**")
    st.markdown("• **대상**: 모바일과 태블릿 사용자 (유지 고객)")
    st.markdown("• **혜택**: 오프라인 다운로드 무제한")
    
    st.markdown("#### **7. 다계정자 특별 강화**")
    st.markdown("• **대상**: 3개 이상 프로필 사용자 (유지 고객)")
    st.markdown("• **혜택**: 프로필 무제한 + 키즈 콘텐츠 무료")
    
    st.markdown("#### **8. 기본 유지 강화**")
    st.markdown("• **대상**: 기타 모든 유지 고객 (churn=0)")
    st.markdown("• **혜택**: AI 개인화 추천 + 25% 할인")

# 프로모션별 분포 통계
st.markdown("---")
st.markdown("## 📊 프로모션별 분포 현황")

# 프로모션별 통계 계산
promotion_counts = customers['추천_프로모션'].value_counts()
total_customers = len(customers)

# 이탈 고객과 유지 고객 분리
churned_customers = customers[customers['churned'] == 1]
retained_customers = customers[customers['churned'] == 0]

# 이탈 고객 프로모션 분포 (분리된 섹션)
st.markdown("### 🔴 이탈 고객 프로모션 분포")
churned_promotion_counts = churned_customers['추천_프로모션'].value_counts()
churned_total = len(churned_customers)

if len(churned_promotion_counts) > 0:
    # 프로모션 이름을 간단히 줄여서 표시
    churned_labels = []
    churned_colors = ['#FF4444', '#FF6666', '#FF8888', '#FFAAAA', '#FFCCCC']
    
    for promo in churned_promotion_counts.index:
        if "연령대별" in promo:
            churned_labels.append("연령대별 할인")
        elif "AI 맞춤" in promo:
            churned_labels.append("AI 맞춤 추천")
        elif "복귀 시" in promo:
            churned_labels.append("장기 미접속자")
        elif "기프트카드" in promo:
            churned_labels.append("결제방법 특화")
        else:
            churned_labels.append("기타")
    
    # 막대 그래프로 표시
    st.markdown("#### 🔴 이탈 고객 프로모션 분포")
    
    # 데이터 준비
    churned_chart_data = pd.DataFrame({
        '고객 수': list(churned_promotion_counts.values)
    }, index=churned_labels)
    
    # 막대 그래프 표시
    st.bar_chart(churned_chart_data, height=400)
    
    # 상세 현황을 더 크고 읽기 쉽게
    st.markdown("#### 📋 이탈 고객 프로모션 상세 현황")
    for promo, count in churned_promotion_counts.items():
        percentage = (count / churned_total * 100)
        st.markdown(f"### 🔴 {promo}")
        st.markdown(f"**{count}명** ({percentage:.1f}%)")
        st.markdown("---")
else:
    st.info("이탈 고객 프로모션 데이터가 없습니다.")

# 유지 고객 프로모션 분포 (분리된 섹션)
st.markdown("### 🟢 유지 고객 프로모션 분포")
retained_promotion_counts = retained_customers['추천_프로모션'].value_counts()
retained_total = len(retained_customers)

if len(retained_promotion_counts) > 0:
    # 프로모션 이름을 간단히 줄여서 표시
    retained_labels = []
    retained_colors = ['#44CC88', '#66DD99', '#88EEAA', '#AAFFBB', '#CCFFCC']
    
    for promo in retained_promotion_counts.index:
        if "프리미엄" in promo:
            retained_labels.append("프리미엄 특화")
        elif "모바일" in promo:
            retained_labels.append("모바일/태블릿")
        elif "다계정" in promo:
            retained_labels.append("다계정 특화")
        elif "기본 유지" in promo:
            retained_labels.append("기본 유지")
        else:
            retained_labels.append("기타")
    
    # 막대 그래프로 표시
    st.markdown("#### 🟢 유지 고객 프로모션 분포")
    
    # 데이터 준비
    retained_chart_data = pd.DataFrame({
        '고객 수': list(retained_promotion_counts.values)
    }, index=retained_labels)
    
    # 막대 그래프 표시
    st.bar_chart(retained_chart_data, height=400)
    
    # 상세 현황을 더 크고 읽기 쉽게
    st.markdown("#### 📋 유지 고객 프로모션 상세 현황")
    for promo, count in retained_promotion_counts.items():
        percentage = (count / retained_total * 100)
        st.markdown(f"### 🟢 {promo}")
        st.markdown(f"**{count}명** ({percentage:.1f}%)")
        st.markdown("---")
else:
    st.info("유지 고객 프로모션 데이터가 없습니다.")

# 전체 통계 요약
st.markdown("### 📋 전체 프로모션 분포 요약")
col3, col4, col5 = st.columns(3)

with col3:
    st.metric("전체 고객 수", f"{total_customers}명")

with col4:
    st.metric("이탈 고객", f"{churned_total}명", f"{churned_total/total_customers*100:.1f}%")

with col5:
    st.metric("유지 고객", f"{retained_total}명", f"{retained_total/total_customers*100:.1f}%")

# 전체 고객 목록
st.markdown("---")
st.subheader("👥 전체 고객 목록")
st.write(f"총 {len(customers)}명의 고객 데이터입니다. (이탈 고객: {len(customers[customers['churned']==1])}명, 유지 고객: {len(customers[customers['churned']==0])}명)")

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
        'churned', '추천_프로모션'
    ]].rename(columns={
        'customer_id': '고객ID',
        'age': '나이',
        'gender': '성별', 
        'subscription_type': '구독타입',
        'watch_hours': '월시청시간',
        'last_login_days': '마지막로그인',
        'payment_method': '결제방법',
        'churned': '이탈상태',
        '추천_프로모션': '추천프로모션'
    }),
    use_container_width=True
)






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