import streamlit as st
import pandas as pd

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

# Netflix 고객 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('data/netflix_customer_churn.csv')

df = load_data()

# 고객 선택 섹션
st.subheader("고객 선택")
st.write("고객을 선택하세요")

# 세션 상태 초기화
if 'selected_customer_id' not in st.session_state:
    st.session_state.selected_customer_id = ""
if 'search_executed' not in st.session_state:
    st.session_state.search_executed = False
if 'sample_id_selected' not in st.session_state:
    st.session_state.sample_id_selected = ""
if 'list_customer_selected' not in st.session_state:
    st.session_state.list_customer_selected = ""

customer_id_input = ""

# 공통 이탈 확률 계산 함수
def calculate_churn_probability_common(customer):
    """고객의 특성을 기반으로 이탈 확률을 계산"""
    base_probability = 40.0  # 기본 확률
    
    # 나이별 위험도
    if customer['age'] < 25:
        base_probability += 15
    elif customer['age'] > 60:
        base_probability += 10
    elif 25 <= customer['age'] <= 40:
        base_probability -= 5
    
    # 구독 타입별 위험도
    if customer['subscription_type'] == 'Basic':
        base_probability += 20
    elif customer['subscription_type'] == 'Premium':
        base_probability -= 15
    elif customer['subscription_type'] == 'Standard':
        base_probability += 5
    
    # 결제 방법별 위험도
    if customer['payment_method'] == 'Gift Card':
        base_probability += 25
    elif customer['payment_method'] == 'Credit Card':
        base_probability -= 10
    elif customer['payment_method'] == 'PayPal':
        base_probability -= 5
    
    # 시청 시간별 위험도
    if customer['watch_hours'] < 5:
        base_probability += 20
    elif customer['watch_hours'] > 20:
        base_probability -= 15
    elif customer['watch_hours'] > 10:
        base_probability -= 5
    
    # 마지막 로그인별 위험도
    if customer['last_login_days'] > 30:
        base_probability += 25
    elif customer['last_login_days'] > 14:
        base_probability += 15
    elif customer['last_login_days'] < 3:
        base_probability -= 10
    
    # 월 구독료별 위험도
    if customer['monthly_fee'] < 5:
        base_probability += 15
    elif customer['monthly_fee'] > 15:
        base_probability -= 10
    
    # 성별별 위험도 (데이터 기반)
    if customer['gender'] == 'Female':
        base_probability += 3
    elif customer['gender'] == 'Other':
        base_probability += 5
    
    # 디바이스별 위험도
    if customer['device'] == 'Tablet':
        base_probability += 8
    elif customer['device'] == 'Smart TV':
        base_probability -= 5
    
    # 프로필 수별 위험도
    if customer['number_of_profiles'] == 1:
        base_probability += 10
    elif customer['number_of_profiles'] >= 4:
        base_probability -= 8
    
    # 확률을 0-100 범위로 제한
    base_probability = max(5, min(95, base_probability))
    
    return round(base_probability, 1)

# 상단 간단 예측 결과 표시
prediction_summary_displayed = False

# 샘플 ID 클릭 결과 표시 (고객 정보 조회 버튼 위)
if st.session_state.sample_id_selected:
    sample_customer_data = df[df['customer_id'] == st.session_state.sample_id_selected]
    if not sample_customer_data.empty:
        sample_customer = sample_customer_data.iloc[0]
        
        st.success(f"✅ 샘플에서 선택된 고객: {st.session_state.sample_id_selected[:20]}...")
        
        # 예측 결과 섹션
        st.subheader("🔍 예측 결과")
        
        sample_churn_rate = calculate_churn_probability_common(sample_customer)
        sample_retention_rate = round(100 - sample_churn_rate, 1)
        
        # 메트릭 표시
        col1, col2 = st.columns(2)
        with col1:
            st.metric("이탈 확률", f"{sample_churn_rate}%")
        with col2:
            st.metric("유지 확률", f"{sample_retention_rate}%")
        
        prediction_summary_displayed = True
        st.divider()

# 다른 방법으로 선택된 고객의 간단 예측 결과 (샘플 ID가 없을 때만 표시)
if not prediction_summary_displayed:
    current_customer_id = ""
    selection_method = ""
    
    # 우선순위: 직접 입력 > 목록 선택
    if st.session_state.search_executed and st.session_state.selected_customer_id:
        current_customer_id = st.session_state.selected_customer_id
        selection_method = "⌨️ 직접 입력"
    elif st.session_state.list_customer_selected:
        current_customer_id = st.session_state.list_customer_selected
        selection_method = "📝 목록에서 선택"
    
    if current_customer_id:
        current_customer_data = df[df['customer_id'] == current_customer_id]
        if not current_customer_data.empty:
            current_customer = current_customer_data.iloc[0]
            
            st.success(f"✅ {selection_method}된 고객: {current_customer_id[:20]}...")
            
            # 예측 결과 섹션
            st.subheader("🔍 예측 결과")
            
            current_churn_rate = calculate_churn_probability_common(current_customer)
            current_retention_rate = round(100 - current_churn_rate, 1)
            
            # 메트릭 표시
            col1, col2 = st.columns(2)
            with col1:
                st.metric("이탈 확률", f"{current_churn_rate}%")
            with col2:
                st.metric("유지 확률", f"{current_retention_rate}%")
            
            st.divider()

# 고객 ID 직접 입력
input_customer_id = st.text_input("CustomerID", 
                                 placeholder="고객 ID를 입력하세요 (예: a9b75100-82a8-427a-a208-72f24052884a)")

if st.button("고객 정보 조회", type="primary", key="search_button"):
    if input_customer_id:
        st.session_state.selected_customer_id = input_customer_id
        st.session_state.search_executed = True
        st.session_state.sample_id_selected = ""
        st.session_state.list_customer_selected = ""
        # st.rerun() 제거 - 버튼 클릭 자체가 페이지를 새로고침함
    else:
        st.error("고객 ID를 입력해주세요.")

# 사용 가능한 고객 ID 샘플 표시
with st.expander("사용 가능한 고객 ID 샘플 보기"):
    st.write("**샘플 고객 ID들:**")
    
    # 전체 고객 ID 목록
    all_customer_ids = df['customer_id'].tolist()
    total_customers = len(all_customer_ids)
    
    # 페이지네이션 설정 (50개씩)
    items_per_page = 50
    total_pages = (total_customers - 1) // items_per_page + 1
    
    # 페이지 선택
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        current_page = st.selectbox(
            f"페이지 선택 (총 {total_pages}페이지, {total_customers}개 고객 ID)",
            range(1, total_pages + 1),
            key="id_page_selector"
        )
    
    # 현재 페이지의 고객 ID 계산
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_customers)
    page_customer_ids = all_customer_ids[start_idx:end_idx]
    
    st.write(f"**{current_page}페이지 ({start_idx + 1}-{end_idx}번째 고객 ID)**")
    
    # 10개씩 한 줄에 표시
    for i in range(0, len(page_customer_ids), 10):
        cols = st.columns(10)
        for j, customer_id in enumerate(page_customer_ids[i:i+10]):
            with cols[j]:
                # 고객 ID를 클릭 가능한 버튼으로 만들기
                button_key = f"id_button_{customer_id}"
                if st.button(customer_id[:8], key=button_key, help=customer_id):
                    # 클릭하면 해당 고객 ID로 예측 실행 (샘플 ID 클릭)
                    if st.session_state.sample_id_selected != customer_id:
                        st.session_state.sample_id_selected = customer_id
                        st.session_state.selected_customer_id = ""
                        st.session_state.list_customer_selected = ""
                        st.session_state.search_executed = False
                        st.rerun()  # 페이지 새로고침하여 예측 결과 표시

st.write("**고객 목록에서 선택하세요:**")

# 필터링 옵션
col1, col2, col3 = st.columns(3)
with col1:
    region_filter = st.selectbox("지역", ["전체"] + sorted(df['region'].unique().tolist()))
with col2:
    subscription_filter = st.selectbox("구독 타입", ["전체"] + sorted(df['subscription_type'].unique().tolist()))
with col3:
    gender_filter = st.selectbox("성별", ["전체"] + sorted(df['gender'].unique().tolist()))

col4, col5, col6 = st.columns(3)
with col4:
    device_filter = st.selectbox("디바이스", ["전체"] + sorted(df['device'].unique().tolist()))
with col5:
    payment_filter = st.selectbox("결제 방법", ["전체"] + sorted(df['payment_method'].unique().tolist()))
with col6:
    genre_filter = st.selectbox("선호 장르", ["전체"] + sorted(df['favorite_genre'].unique().tolist()))


# 필터 적용
filtered_df = df.copy()

if region_filter != "전체":
    filtered_df = filtered_df[filtered_df['region'] == region_filter]

if subscription_filter != "전체":
    filtered_df = filtered_df[filtered_df['subscription_type'] == subscription_filter]

if gender_filter != "전체":
    filtered_df = filtered_df[filtered_df['gender'] == gender_filter]

if device_filter != "전체":
    filtered_df = filtered_df[filtered_df['device'] == device_filter]

if payment_filter != "전체":
    filtered_df = filtered_df[filtered_df['payment_method'] == payment_filter]

if genre_filter != "전체":
    filtered_df = filtered_df[filtered_df['favorite_genre'] == genre_filter]


# 고객 정보를 보기 좋게 표시하기 위한 포맷팅
customer_options = []
customer_mapping = {}

# 최대 100명까지 표시
display_df = filtered_df.head(100)

if len(display_df) == 0:
    st.warning("선택한 조건에 맞는 고객이 없습니다.")
    customer_id_input = ""
else:
    st.info(f"조건에 맞는 고객 {len(filtered_df)}명 중 {len(display_df)}명을 표시합니다.")
    
    for idx, row in display_df.iterrows():
        display_text = f"{row['customer_id'][:8]}... | {row['age']}세 {row['gender']} | {row['subscription_type']} | {row['region']} | {row['device']} | {row['payment_method']} | {row['favorite_genre']}"
        customer_options.append(display_text)
        customer_mapping[display_text] = row['customer_id']
    
    selected_customer_display = st.selectbox(
        "고객 선택",
        options=["선택하세요..."] + customer_options,
        key="customer_selectbox"
    )
    
    if selected_customer_display != "선택하세요...":
        # 이전에 선택된 고객과 다른 경우에만 상태 업데이트
        selected_id = customer_mapping[selected_customer_display]
        if st.session_state.list_customer_selected != selected_id:
            st.session_state.list_customer_selected = selected_id
            st.session_state.selected_customer_id = ""
            st.session_state.search_executed = False
            # 목록에서 선택했을 때는 샘플 ID도 초기화하여 새로운 선택이 위에 반영되도록 함
            st.session_state.sample_id_selected = ""

# 직접 입력, 샘플 ID 선택, 또는 고객 목록 선택 결과 처리
if st.session_state.search_executed and st.session_state.selected_customer_id:
    customer_id_input = st.session_state.selected_customer_id
elif st.session_state.sample_id_selected:
    customer_id_input = st.session_state.sample_id_selected  # 샘플 ID도 아래에 상세 표시
elif st.session_state.list_customer_selected:
    customer_id_input = st.session_state.list_customer_selected
else:
    customer_id_input = ""

# 선택된 고객 정보 표시 (아래쪽 - 상세)
if customer_id_input:
    # 입력된 고객 ID로 고객 찾기
    customer_data = df[df['customer_id'] == customer_id_input]
    
    if not customer_data.empty:
        customer = customer_data.iloc[0]
        
        # 선택 방법에 따른 제목 표시
        if st.session_state.sample_id_selected and customer_id_input == st.session_state.sample_id_selected:
            st.info(f"📋 샘플 ID에서 선택된 고객: {customer_id_input[:20]}...")
        elif st.session_state.list_customer_selected and customer_id_input == st.session_state.list_customer_selected:
            st.info(f"📝 목록에서 선택된 고객: {customer_id_input[:20]}...")
        elif st.session_state.selected_customer_id and customer_id_input == st.session_state.selected_customer_id:
            st.info(f"⌨️ 직접 입력된 고객: {customer_id_input[:20]}...")
        
        # 예측 결과 섹션
        st.subheader("📊 상세 예측 결과")
        
        # 공통 함수를 사용하여 이탈 확률 계산
        churn_rate = calculate_churn_probability_common(customer)
        retention_rate = round(100 - churn_rate, 1)
        
        # 메트릭 표시
        col1, col2 = st.columns(2)
        with col1:
            st.metric("이탈 확률", f"{churn_rate}%")
        with col2:
            st.metric("유지 확률", f"{retention_rate}%")
        
        # 이탈/유지 확률 차트
        st.subheader("이탈/유지 확률")
        
        # 위험도에 따른 동적 색상 설정
        if churn_rate >= 70:
            churn_color = "#DC143C"  # 진한 빨간색 (매우 위험)
            risk_emoji = "🔴"
        elif churn_rate >= 50:
            churn_color = "#FF4500"  # 주황빨간색 (높은 위험)
            risk_emoji = "🟠"
        elif churn_rate >= 30:
            churn_color = "#FF6347"  # 토마토색 (보통 위험)
            risk_emoji = "🟡"
        else:
            churn_color = "#32CD32"  # 라임그린 (낮은 위험)
            risk_emoji = "🟢"
        
        # 색상으로 구분된 차트 (CSS 스타일 사용)
        st.markdown(f"""
        <style>
        .churn-bar {{
            background-color: {churn_color};
            color: white;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        .retention-bar {{
            background-color: #1f77b4;
            color: white;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .probability-container {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # 확률 표시 컨테이너
        st.markdown('<div class="probability-container">', unsafe_allow_html=True)
        
        # 이탈 확률 바 (동적 크기)
        churn_width = max(80, int(churn_rate * 4))  # 최소 80px, 최대 380px
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 15px 0;">
            <div style="width: 100px; font-weight: bold; font-size: 16px;">{risk_emoji} 이탈:</div>
            <div class="churn-bar" style="width: {churn_width}px; min-width: 100px;">
                {churn_rate}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 유지 확률 바 (동적 크기)
        retention_width = max(80, int(retention_rate * 4))  # 최소 80px, 최대 380px
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 15px 0;">
            <div style="width: 100px; font-weight: bold; font-size: 16px;">✅ 유지:</div>
            <div class="retention-bar" style="width: {retention_width}px; min-width: 100px;">
                {retention_rate}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 상세 고객 정보 (접힌 형태로)
        with st.expander("상세 고객 정보 보기"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**고객 ID:** {customer['customer_id']}")
                st.write(f"**나이:** {customer['age']}세")
                st.write(f"**성별:** {customer['gender']}")
                st.write(f"**구독 타입:** {customer['subscription_type']}")
                st.write(f"**지역:** {customer['region']}")
                st.write(f"**디바이스:** {customer['device']}")
            
            with col2:
                st.write(f"**월 시청 시간:** {customer['watch_hours']:.1f}시간")
                st.write(f"**마지막 로그인:** {customer['last_login_days']}일 전")
                st.write(f"**월 구독료:** ${customer['monthly_fee']}")
                st.write(f"**결제 방법:** {customer['payment_method']}")
                st.write(f"**프로필 수:** {customer['number_of_profiles']}")
                st.write(f"**선호 장르:** {customer['favorite_genre']}")
        
        # 이탈 위험 요소 분석
        st.subheader("🚨 주요 위험 요소 분석")
        
        risk_factors = []
        protection_factors = []
        
        # 위험 요소 분석
        if customer['payment_method'] == 'Gift Card':
            risk_factors.append("기프트카드 결제 (만료 위험)")
        if customer['last_login_days'] > 30:
            risk_factors.append("30일 이상 미접속 (매우 높은 위험)")
        elif customer['last_login_days'] > 14:
            risk_factors.append("14일 이상 미접속 (높은 위험)")
        if customer['watch_hours'] < 5:
            risk_factors.append("낮은 시청 시간 (월 5시간 미만)")
        if customer['age'] < 25:
            risk_factors.append("젊은 연령층 (변동성 높음)")
        elif customer['age'] > 60:
            risk_factors.append("고령층 (기술 적응 어려움)")
        if customer['subscription_type'] == 'Basic':
            risk_factors.append("기본 요금제 (기능 제한)")
        if customer['monthly_fee'] < 5:
            risk_factors.append("낮은 구독료 (가치 인식 부족)")
        if customer['device'] == 'Tablet':
            risk_factors.append("태블릿 사용 (불편한 시청 환경)")
        if customer['number_of_profiles'] == 1:
            risk_factors.append("단일 프로필 (가족 공유 미활용)")
        
        # 보호 요소 분석
        if customer['subscription_type'] == 'Premium':
            protection_factors.append("프리미엄 구독 (높은 만족도)")
        if customer['watch_hours'] > 20:
            protection_factors.append("높은 시청 시간 (적극적 이용)")
        elif customer['watch_hours'] > 10:
            protection_factors.append("적정 시청 시간 (안정적 이용)")
        if customer['last_login_days'] < 3:
            protection_factors.append("최근 접속 (활발한 이용)")
        if customer['payment_method'] == 'Credit Card':
            protection_factors.append("신용카드 결제 (안정적 결제)")
        if 25 <= customer['age'] <= 40:
            protection_factors.append("핵심 연령층 (안정적 이용 패턴)")
        if customer['device'] == 'Smart TV':
            protection_factors.append("스마트 TV 이용 (편리한 시청 환경)")
        if customer['number_of_profiles'] >= 4:
            protection_factors.append("다중 프로필 (가족 공유 활용)")
        if customer['monthly_fee'] > 15:
            protection_factors.append("높은 구독료 (서비스 가치 인정)")
        
        # 위험 요소 표시
        if risk_factors:
            st.error("🚨 **위험 요소**")
            for factor in risk_factors:
                st.write(f"• {factor}")
        
        # 보호 요소 표시
        if protection_factors:
            st.success("✅ **보호 요소**")
            for factor in protection_factors:
                st.write(f"• {factor}")
        
        # 종합 위험도 평가
        risk_level = ""
        if churn_rate >= 70:
            risk_level = "🔴 **매우 높음** - 즉시 대응 필요"
        elif churn_rate >= 50:
            risk_level = "🟠 **높음** - 적극적 관리 필요"
        elif churn_rate >= 30:
            risk_level = "🟡 **보통** - 주기적 모니터링 필요"
        else:
            risk_level = "🟢 **낮음** - 안정적 고객"
        
        st.info(f"**종합 위험도:** {risk_level}")
        
    else:
        st.error("해당 고객 ID를 찾을 수 없습니다. 올바른 고객 ID를 입력해주세요.")




#################
# Side Bar 설정 #
#################
# 각각의 페이지로 넘어가도록 연결하기
st.sidebar.header("🚀페이지 이동🚀")
st.sidebar.page_link("app.py", label="📍기본 페이지📍")
st.sidebar.page_link("pages/1 Prediction.py", label="🔎고객 이탈 확률 예측🔎")
st.sidebar.page_link("pages/2 Recommendations.py", label="🪄프로모션 추천🪄")
st.sidebar.success("🙋🏻버튼을 클릭하여 원하는 기능을 사용해보세요!💁🏻‍♀️")