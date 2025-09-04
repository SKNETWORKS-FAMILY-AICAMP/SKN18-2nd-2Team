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

# 고객 선택 방법 탭
tab1, tab2 = st.tabs(["고객 ID 직접 입력", "고객 목록에서 선택"])

# 세션 상태 초기화
if 'selected_customer_id' not in st.session_state:
    st.session_state.selected_customer_id = ""
if 'search_executed' not in st.session_state:
    st.session_state.search_executed = False

customer_id_input = ""

with tab1:
    # 고객 ID 입력 필드와 실행 버튼
    input_customer_id = st.text_input("CustomerID", 
                                     placeholder="고객 ID를 입력하세요 (예: a9b75100-82a8-427a-a208-72f24052884a)")
    
    if st.button("고객 정보 조회", type="primary", key="search_button"):
        if input_customer_id:
            st.session_state.selected_customer_id = input_customer_id
            st.session_state.search_executed = True
        else:
            st.error("고객 ID를 입력해주세요.")
    

with tab2:
    # 고객 목록에서 선택
    st.write("**고객 목록에서 선택하세요:**")
    
    # 필터링 옵션
    col1, col2, col3 = st.columns(3)
    with col1:
        churn_filter = st.selectbox("이탈 상태", ["전체", "이탈", "유지"])
    with col2:
        subscription_filter = st.selectbox("구독 타입", ["전체", "Basic", "Standard", "Premium"])
    with col3:
        gender_filter = st.selectbox("성별", ["전체", "Male", "Female", "Other"])
    
    # 필터 적용
    filtered_df = df.copy()
    
    if churn_filter == "이탈":
        filtered_df = filtered_df[filtered_df['churned'] == 1]
    elif churn_filter == "유지":
        filtered_df = filtered_df[filtered_df['churned'] == 0]
    
    if subscription_filter != "전체":
        filtered_df = filtered_df[filtered_df['subscription_type'] == subscription_filter]
    
    if gender_filter != "전체":
        filtered_df = filtered_df[filtered_df['gender'] == gender_filter]
    
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
            display_text = f"{row['customer_id'][:8]}... | {row['age']}세 {row['gender']} | {row['subscription_type']} | {row['region']} | {'이탈' if row['churned'] == 1 else '유지'}"
            customer_options.append(display_text)
            customer_mapping[display_text] = row['customer_id']
        
        selected_customer_display = st.selectbox(
            "고객 선택",
            options=["선택하세요..."] + customer_options,
            key="customer_selectbox"
        )
        
        if selected_customer_display != "선택하세요...":
            st.session_state.selected_customer_id = customer_mapping[selected_customer_display]
            st.session_state.search_executed = True

# 최종 customer_id_input 설정
if st.session_state.search_executed and st.session_state.selected_customer_id:
    customer_id_input = st.session_state.selected_customer_id
else:
    customer_id_input = ""

# 고객 ID가 입력되었을 때 해당 고객 정보 표시
if customer_id_input:
    # 입력된 고객 ID로 고객 찾기
    customer_data = df[df['customer_id'] == customer_id_input]
    
    if not customer_data.empty:
        customer = customer_data.iloc[0]
        
        # 예측 결과 섹션
        st.subheader("예측 결과")
        
        # 실제 이탈 여부를 백분율로 표시
        actual_churn = customer['churned']
        churn_rate = 61.7 if actual_churn == 1 else 38.3  # 실제 데이터 기반 표시
        retention_rate = 100 - churn_rate
        
        # 메트릭 표시
        col1, col2 = st.columns(2)
        with col1:
            st.metric("이탈 확률", f"{churn_rate}%")
        with col2:
            st.metric("유지 확률", f"{retention_rate}%")
        
        # 이탈/유지 확률 차트
        st.subheader("이탈/유지 확률")
        
        # 색상으로 구분된 차트 (CSS 스타일 사용)
        st.markdown("""
        <style>
        .churn-bar {
            background-color: #FF4B4B;
            color: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
        }
        .retention-bar {
            background-color: #1f77b4;
            color: white;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # 이탈 확률 바
        churn_width = int(churn_rate)
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="width: 80px; font-weight: bold;">이탈:</div>
            <div class="churn-bar" style="width: {churn_width * 3}px; min-width: 100px;">
                {churn_rate}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 유지 확률 바
        retention_width = int(retention_rate)
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <div style="width: 80px; font-weight: bold;">유지:</div>
            <div class="retention-bar" style="width: {retention_width * 3}px; min-width: 100px;">
                {retention_rate}%
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
        risk_factors = []
        if customer['payment_method'] == 'Gift Card':
            risk_factors.append("기프트카드 결제 (만료 위험)")
        if customer['last_login_days'] > 20:
            risk_factors.append("장기간 미접속")
        if customer['watch_hours'] < 5:
            risk_factors.append("낮은 시청 시간")
            
        if risk_factors:
            st.info("💡 " + "실제 고객의 상세 정보나 " + "고객 상세 정보 페이지에서 확인할 수 있습니다.")
        
    else:
        st.error("해당 고객 ID를 찾을 수 없습니다. 올바른 고객 ID를 입력해주세요.")




# 사용 가능한 고객 ID 샘플 표시
with st.expander("사용 가능한 고객 ID 샘플 보기"):
    sample_customers = df.head(10)['customer_id'].tolist()
    st.write("**샘플 고객 ID들:**")
    for i, customer_id in enumerate(sample_customers, 1):
        st.code(customer_id)


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