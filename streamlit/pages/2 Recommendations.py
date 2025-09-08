import os, sys
import streamlit as st
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from modeling.utils import get_config
from con_database.database import Database
from sidebar_utils import *

###############################
# 프로모션 추천 페이지 만들기 #
###############################

# 1. 이탈 가능성이 높은 고객 리스트
#     - 이탈 가능성이 높은 고객을 그래프로 보여주기
# 2. 프로모션 추천
#     - 각 고객별로 맞춤형 프로모션을 추천 
#     ex) 할인, 기프트카드 등등

st.title("🪄분석 및 프로모션 추천🪄")
st.session_state["current_page"] = "recommend"

# Netflix 고객 데이터 로드
config = get_config()
db_instance = Database(**config["database"])
db_instance.connect()
rows, cols = db_instance.read_all_data()

df = pd.DataFrame(rows, columns=cols)

# 이탈한 고객들만 필터링하고 프로모션 추천 로직 추가
def get_churned_customers_with_promotions():
    churned_customers = df[df['churned'] == 1].copy()
    
    # 업그레이드된 프로모션 추천 로직 (이탈 고객 대상)
    def recommend_promotion(row):
        # 1. 연령별 이탈 방지
        # 대상: 20~30대 그리고 40대 중반에서 60대초반
        if (20 <= row['age'] <= 35) or (45 <= row['age'] <= 65):
            return "🎂 연령대별 특별 할인 30% + 1주일 무료 체험"
        
        # 2. 월 시청시간 저조자 이탈 방지
        # 대상: 월 시청시간 5시간 미만인자
        elif row['watch_hours'] < 5:
            return "📺 무료 AI 맞춤 서비스 제공 + 1주일 무료 체험"
        
        # 3. 장기 미접속자 복귀 유인
        # 대상: 30일 이상 미접속자
        elif row['last_login_days'] >= 30:
            return "⏰ 복귀 시 최대 70% 할인 + 무료 AI 맞춤 서비스 제공 + 1주일 무료 체험"
        
        # 4. 결제 방법 불편 해소
        # 대상: Gift Card와 Crypto 결제자
        elif row['payment_method'] in ['Gift Card', 'Crypto']:
            if row['payment_method'] == 'Gift Card':
                return "🎁 cradit card 으로 결제 방법 변경 시 첫 결제 할인 혜택"
            else:  # Crypto
                return "💰 cradit card 으로 결제 방법 변경 시 첫 결제 할인 혜택"
        
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
            return "🎯 기본 복귀 혜택: 무료 AI 맞춤 서비스 제공"
    
    # 프로모션 추천 적용
    churned_customers['추천_프로모션'] = churned_customers.apply(recommend_promotion, axis=1)    
    return churned_customers

# 전체 고객 데이터 로드 및 프로모션 적용
def get_all_customers_with_promotions():
    all_customers = df.copy()
    
    # 이탈 고객과 비이탈 고객에 따라 다른 프로모션 적용
    def recommend_promotion_all(row):
        if row['churned'] == 1:  # 이탈 고객
            # 4개 프로모션 로직 - 우선순위 조정으로 고른 분포
            if row['last_login_days'] >= 30:
                return "🔴 장기 미접속자 복귀 유인: 즉시 복귀 시 60% 할인 + 1주 무료체험 + 맞춤 콘텐츠 추천"
            elif row['watch_hours'] < 5:
                return "🔴 월 시청시간 저조자: 무료 AI 맞춤 서비스 제공 + 1주일 무료 체험"
            elif (20 <= row['age'] <= 30) or (45 <= row['age'] <= 60):
                return "🔴 연령대별 할인: 이탈률이 높은 연령대 대상 30% 할인 + 연령대 맞춤 콘텐츠"
            elif row['payment_method'] in ['Gift Card', 'Crypto']:
                return "🔴 결제방법 특화: cradit card 으로 결제 방법 변경 시 첫 결제 할인 혜택"
            else:
                return "🔴 장기 미접속자 복귀 유인: 즉시 복귀 시 60% 할인 + 2주 무료 체험 + 맞춤 콘텐츠 추천"
        else:  # 비이탈 고객 (churned == 0)
            # 유지 고객 대상 프로모션 로직
            if row['subscription_type'] == 'Premium' or row['monthly_fee'] > 15:
                return "🟢 프리미엄 고객 전용: 4K 콘텐츠 무제한 + 일주일 무료"
            elif row['device'] in ['Mobile', 'Tablet']:
                return "🟢 모바일/태블릿 전용: 오프라인 다운로드 무제한"
            elif row['number_of_profiles'] >= 3:
                return "🟢 다계정 특별 혜택: 프로필 무제한 + 키즈 콘텐츠 무료"
            else:
                return "🟢 기본 유지 강화: 무료 AI 맞춤 서비스 제공"
    
    # 프로모션 추천 적용
    all_customers['추천_프로모션'] = all_customers.apply(recommend_promotion_all, axis=1)
    
    return all_customers

customers = get_all_customers_with_promotions()

# 탭 생성
tab1, tab2 = st.tabs(["📊 이탈자 데이터 분석", "🪄 프로모션 추천"])

with tab1:
    st.header("📊 이탈자 데이터 분석")
    
    # Netflix 고객 데이터 로드 (이미 위에서 로드되었지만 탭 내에서 다시 사용)
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

    # 주요 Feature별 이탈률 분석
    st.subheader("📊 주요 Feature별 이탈률 분석")

    # 1. 월 시청시간별 이탈률
    st.write("**📺 월 시청시간별 이탈률**")
    df['watch_hours_category'] = pd.cut(df['watch_hours'], 
                                       bins=[0, 2, 5, 10, 20, float('inf')], 
                                       labels=['0-2시간', '2-5시간', '5-10시간', '10-20시간', '20시간+'])

    watch_category_churn = df.groupby('watch_hours_category').agg({
        'churned': ['count', 'sum']
    }).round(2)
    watch_category_churn.columns = ['총고객수', '이탈고객수']
    watch_category_churn['이탈률(%)'] = (watch_category_churn['이탈고객수'] / watch_category_churn['총고객수'] * 100).round(1)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(watch_category_churn['이탈률(%)'])
    with col2:
        st.dataframe(watch_category_churn)

    # 2. 마지막 로그인 일수별 이탈률
    st.write("**🕐 마지막 로그인 일수별 이탈률**")
    df['login_category'] = pd.cut(df['last_login_days'], 
                                 bins=[0, 7, 14, 30, 60, 1000], 
                                 labels=['1주일 이내', '1-2주', '2-4주', '1-2개월', '2개월+'])

    login_category_churn = df.groupby('login_category').agg({
        'churned': ['count', 'sum']
    }).round(2)
    login_category_churn.columns = ['총고객수', '이탈고객수']
    login_category_churn['이탈률(%)'] = (login_category_churn['이탈고객수'] / login_category_churn['총고객수'] * 100).round(1)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(login_category_churn['이탈률(%)'])
    with col2:
        st.dataframe(login_category_churn)

    # 3. 결제 방법별 이탈률
    st.write("**💳 결제 방법별 이탈률**")
    payment_churn = df.groupby('payment_method').agg({
        'churned': ['count', 'sum']
    }).round(2)
    payment_churn.columns = ['총고객수', '이탈고객수']
    payment_churn['이탈률(%)'] = (payment_churn['이탈고객수'] / payment_churn['총고객수'] * 100).round(1)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(payment_churn['이탈률(%)'])
    with col2:
        st.dataframe(payment_churn)

    # 4. 디바이스별 이탈률
    st.write("**📱 디바이스별 이탈률**")
    device_churn = df.groupby('device').agg({
        'churned': ['count', 'sum']
    }).round(2)
    device_churn.columns = ['총고객수', '이탈고객수']
    device_churn['이탈률(%)'] = (device_churn['이탈고객수'] / device_churn['총고객수'] * 100).round(1)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(device_churn['이탈률(%)'])
    with col2:
        st.dataframe(device_churn)

    # 5. 구독 타입별 이탈률
    st.write("**📦 구독 타입별 이탈률**")
    subscription_churn = df.groupby('subscription_type').agg({
        'churned': ['count', 'sum']
    }).round(2)
    subscription_churn.columns = ['총고객수', '이탈고객수']
    subscription_churn['이탈률(%)'] = (subscription_churn['이탈고객수'] / subscription_churn['총고객수'] * 100).round(1)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(subscription_churn['이탈률(%)'])
    with col2:
        st.dataframe(subscription_churn)

    # 핵심 인사이트
    st.subheader("💡핵심 인사이트")
    st.write("**주요 발견사항:**")

    # 5개 주요 feature별 최고 이탈률 찾기
    highest_watch_churn = watch_category_churn['이탈률(%)'].idxmax()
    highest_watch_rate = watch_category_churn.loc[highest_watch_churn, '이탈률(%)']
    
    highest_login_churn = login_category_churn['이탈률(%)'].idxmax()
    highest_login_rate = login_category_churn.loc[highest_login_churn, '이탈률(%)']
    
    highest_payment_churn = payment_churn['이탈률(%)'].idxmax()
    highest_payment_rate = payment_churn.loc[highest_payment_churn, '이탈률(%)']
    
    highest_device_churn = device_churn['이탈률(%)'].idxmax()
    highest_device_rate = device_churn.loc[highest_device_churn, '이탈률(%)']
    
    highest_sub_churn = subscription_churn['이탈률(%)'].idxmax()
    highest_sub_rate = subscription_churn.loc[highest_sub_churn, '이탈률(%)']

    # 위험 요소별 정리
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("🔴 **최고 위험 세그먼트:**")
        st.write(f"- **{highest_watch_churn}** 시청: **{highest_watch_rate}%** 이탈률")
        st.write(f"- **{highest_login_churn}** 접속: **{highest_login_rate}%** 이탈률")
        st.write(f"- **{highest_payment_churn}** 결제: **{highest_payment_rate}%** 이탈률")
    
    with col2:
        st.write("⚠️ **주의 세그먼트:**")
        st.write(f"- **{highest_device_churn}** 디바이스: **{highest_device_rate}%** 이탈률")
        st.write(f"- **{highest_sub_churn}** 구독: **{highest_sub_rate}%** 이탈률")

    st.write("**📈 5개 핵심 Feature 기반 개선 전략:**")
    
    # 개선 방안을 2열로 배치
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 사용 패턴 최적화:**")
        st.write("- 📺 **시청시간 증대**: 저시청 그룹 맞춤 콘텐츠 추천")
        st.write("- 🕐 **접속 빈도 관리**: 미접속자 조기 발견 및 재참여 유도")
        st.write("- 📱 **디바이스별 UX**: 플랫폼 특성에 맞는 인터페이스 제공")
    
    with col2:
        st.write("**💼 서비스 구조 개선:**")
        st.write("- 💳 **결제 방법 안정화**: 다른 결제 수단으로 전환시 혜택 제공으로 결제방법 변경 유도")
        st.write("- 📦 **구독 플랜 최적화**: 고이탈 플랜의 가치 제안 강화")
        st.write("- 🎯 **통합 리텐션 전략**: 5개 핵심 지표 기반 예측 모델 구축")

with tab2:
    # 💡 업그레이드된 프로모션 추천 전략
    st.markdown("## 💡 업그레이드된 프로모션 추천 전략")

    col_strategy1, col_strategy2 = st.columns(2)

    with col_strategy1:
        st.markdown("### 🎯 **이탈 고객 대상 전략**")
        
        st.markdown("#### **1. 월 시청시간 저조자 이탈 방지**")
        st.markdown("• **대상**: 월 시청시간 5시간 미만 (이탈 고객)")
        st.markdown("• **혜택**: 무료 AI 맞춤 서비스 제공 + 1주일 무료 체험")
        
        st.markdown("#### **2. 장기 미접속자 복귀 유인**")
        st.markdown("• **대상**: 30일 이상 미접속자 (이탈 고객)")
        st.markdown("• **혜택**: 복귀 시 최대 70% 할인 + 무료 AI 맞춤 서비스 제공 + 1주일 무료 체험")
        
        st.markdown("#### **3. 결제 방법 불편 해소**")
        st.markdown("• **대상**: Gift Card와 Crypto 결제자 (이탈 고객)")
        st.markdown("• **혜택**: cradit card 으로 결제 방법 변경 시 첫 결제 할인 혜택")

    with col_strategy2:
        st.markdown("### 🚀 **유지 대상 고객 전략**")
        
        st.markdown("#### **4. 프리미엄 고객 집중 강화**")
        st.markdown("• **대상**: Premium 구독자 및 고액결제자 (유지 고객)")
        st.markdown("• **혜택**: 4K 콘텐츠 무제한 + 요금제 할인쿠폰 제공")
        
        st.markdown("#### **5. 기본 유지 강화**")
        st.markdown("• **대상**: 기타 모든 유지 고객")
        st.markdown("• **혜택**: 무료 AI 맞춤 서비스 제공")

    # 이탈 및 유지 프로모션 비율 계산
    st.markdown("---")
    st.markdown("## 📊 이탈 및 유지 프로모션 비율")
    
    # 이탈 고객과 유지 고객 분리
    churned_customers = customers[customers['churned'] == 1]
    retained_customers = customers[customers['churned'] == 0]
    total_customers = len(churned_customers) + len(retained_customers)
    
    # 전체 비율 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("전체 고객 수", f"{total_customers:,}명")
    with col2:
        churn_rate = (len(churned_customers) / total_customers * 100) if total_customers > 0 else 0
        st.metric("이탈 고객", f"{len(churned_customers):,}명", f"{churn_rate:.1f}%")
    with col3:
        retention_rate = (len(retained_customers) / total_customers * 100) if total_customers > 0 else 0
        st.metric("유지 고객", f"{len(retained_customers):,}명", f"{retention_rate:.1f}%")

    # 이탈 고객 프로모션 분석
    st.markdown("### 🔴 이탈 고객 프로모션 분석")

    if len(churned_customers) > 0:
        churned_total = len(churned_customers)
        churned_promotion_counts = churned_customers['추천_프로모션'].value_counts()
        
        # 3개 프로모션 분류 (연령대별 제외)
        churned_simplified = {}
        for promo, count in churned_promotion_counts.items():
            if "장기 미접속자" in promo:
                if "장기 미접속자" in churned_simplified:
                    churned_simplified["장기 미접속자"] += count
                else:
                    churned_simplified["장기 미접속자"] = count
            elif "시청시간 저조자" in promo:
                churned_simplified["월 시청시간 저조자"] = count
            elif "결제방법" in promo:
                churned_simplified["결제방법 특화"] = count
            else:
                # 기타는 장기 미접속자에 통합
                if "장기 미접속자" in churned_simplified:
                    churned_simplified["장기 미접속자"] += count
                else:
                    churned_simplified["장기 미접속자"] = count
        
        st.markdown("#### 📊 이탈 프로모션 비율")
        
        # 각 프로모션별 간략한 소개와 퍼센트
        for promo_name, count in churned_simplified.items():
            percentage = (count / churned_total * 100)
            
            if promo_name == "장기 미접속자":
                st.markdown(f"**🔴 {promo_name}**: 30일 이상 미접속자 및 기타 이탈 고객 복귀 유인 - **<span style='font-size: 20px; font-weight: bold; color: #FF4444;'>{percentage:.1f}%</span>** ({count}명)", unsafe_allow_html=True)
            elif promo_name == "월 시청시간 저조자":
                st.markdown(f"**🔴 {promo_name}**: 월 시청시간 5시간 미만 저조자 대상 - **<span style='font-size: 20px; font-weight: bold; color: #FF4444;'>{percentage:.1f}%</span>** ({count}명)", unsafe_allow_html=True)
            elif promo_name == "결제방법 특화":
                st.markdown(f"**🔴 {promo_name}**: 기프트카드/암호화폐 결제자 대상 - **<span style='font-size: 20px; font-weight: bold; color: #FF4444;'>{percentage:.1f}%</span>** ({count}명)", unsafe_allow_html=True)
    else:
        st.info("이탈 고객 데이터가 없습니다.")

    # 유지 고객 프로모션 분석
    st.markdown("### 🟢 유지 고객 프로모션 분석")

    if len(retained_customers) > 0:
        retained_total = len(retained_customers)
        retained_promotion_counts = retained_customers['추천_프로모션'].value_counts()
        
        # 프로모션 이름 간단화 (2개 전략만 남음)
        retained_simplified = {}
        for promo, count in retained_promotion_counts.items():
            if "프리미엄" in promo:
                retained_simplified["프리미엄 특화"] = count
            elif "기본 유지" in promo:
                if "기본 유지" in retained_simplified:
                    retained_simplified["기본 유지"] += count
                else:
                    retained_simplified["기본 유지"] = count
            else:
                # 기타는 기본 유지에 통합
                if "기본 유지" in retained_simplified:
                    retained_simplified["기본 유지"] += count
                else:
                    retained_simplified["기본 유지"] = count
        
        st.markdown("#### 📊 유지 프로모션 비율")
        
        # 각 프로모션별 간략한 소개와 퍼센트
        for promo_name, count in retained_simplified.items():
            percentage = (count / retained_total * 100)
            
            if promo_name == "프리미엄 특화":
                st.markdown(f"**🟢 {promo_name}**: Premium 구독자 및 고액결제자 대상 - **<span style='font-size: 20px; font-weight: bold; color: #4CAF50;'>{percentage:.1f}%</span>** ({count}명)", unsafe_allow_html=True)
            elif promo_name == "기본 유지":
                st.markdown(f"**🟢 {promo_name}**: 기타 모든 유지 고객 대상 기본 혜택 - **<span style='font-size: 20px; font-weight: bold; color: #4CAF50;'>{percentage:.1f}%</span>** ({count}명)", unsafe_allow_html=True)
    else:
        st.info("유지 고객 데이터가 없습니다.")


    # 전체 고객 목록
    st.markdown("---")
    st.subheader("👥 전체 고객 목록")
    st.write(f"총 {len(customers)}명의 고객 데이터입니다. (이탈 고객: {len(customers[customers['churned']==1])}명, 유지 고객: {len(customers[customers['churned']==0])}명)")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        # 페이지네이션 설정
        items_per_page = st.selectbox("페이지당 표시 개수", [20, 50, 100, 200], index=0)
        total_pages = (len(customers) - 1) // items_per_page + 1
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

setup_css_styles(), login_button(), set_sidebar(), ad()