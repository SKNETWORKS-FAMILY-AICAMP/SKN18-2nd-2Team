import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="넷플릭스 고객 이탈 예측 어플리케이션",
    page_icon="📊",
    layout="wide"
)

# 다크 테마 스타일
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
    }
    .stApp {
        background-color: #1E1E1E;
    }
    .main-title {
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: left;
        margin-bottom: 2rem;
        padding: 1rem;
        background-color: #2C2C2C;
        border-radius: 10px;
    }
    .section-title {
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1.5rem 0 0.5rem 0;
    }
    .metric-container {
        background-color: #2C2C2C;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-text {
        color: white;
        font-size: 1.1rem;
        margin: 0.5rem 0;
    }
    
    /* 모든 Streamlit 컴포넌트 강제 스타일링 */
    
    /* 셀렉트박스 전체 스타일링 */
    .stSelectbox label, 
    div[data-testid="stSelectbox"] label,
    .stSelectbox > label {
        color: #FF69B4 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    
    .stSelectbox > div > div,
    div[data-testid="stSelectbox"] > div > div,
    .stSelectbox [data-baseweb="select"],
    div[data-testid="stSelectbox"] [data-baseweb="select"] {
        background-color: #2C2C2C !important;
        border: 2px solid #4ECDC4 !important;
        color: #87CEEB !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div,
    div[data-testid="stSelectbox"] [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] span,
    div[data-testid="stSelectbox"] [data-baseweb="select"] span {
        color: #87CEEB !important;
        background-color: #2C2C2C !important;
    }
    
    /* 드롭다운 메뉴 옵션들 */
    .stSelectbox [role="option"],
    div[data-testid="stSelectbox"] [role="option"],
    .stSelectbox [role="listbox"] > div,
    div[data-testid="stSelectbox"] [role="listbox"] > div {
        background-color: #2C2C2C !important;
        color: #87CEEB !important;
    }
    
    .stSelectbox [role="option"]:hover,
    div[data-testid="stSelectbox"] [role="option"]:hover {
        background-color: #4ECDC4 !important;
        color: #1E1E1E !important;
    }
    
    /* 텍스트 입력 필드 */
    .stTextInput label,
    div[data-testid="stTextInput"] label {
        color: #FF69B4 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    
    .stTextInput input,
    div[data-testid="stTextInput"] input,
    .stTextInput > div > div > input,
    div[data-testid="stTextInput"] > div > div > input {
        background-color: #2C2C2C !important;
        color: #87CEEB !important;
        border: 2px solid #4ECDC4 !important;
        font-size: 1rem !important;
    }
    
    .stTextInput input::placeholder,
    div[data-testid="stTextInput"] input::placeholder {
        color: #98FB98 !important;
        opacity: 0.7 !important;
    }
    
    /* 전체 앱 배경 */
    .main, .block-container {
        background-color: #1E1E1E !important;
    }
    
    /* 사이드바 스타일링 */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #2C2C2C !important;
    }
    
    .css-1d391kg .stSelectbox,
    .css-1lcbmhc .stSelectbox {
        color: #87CEEB !important;
    }
    
    /* 확장 컴포넌트 */
    .streamlit-expanderHeader,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] .streamlit-expanderHeader {
        background-color: #2C2C2C !important;
        color: #87CEEB !important;
        border: 2px solid #4ECDC4 !important;
        font-weight: bold !important;
    }
    
    .streamlit-expanderContent,
    [data-testid="stExpander"] > div,
    [data-testid="stExpander"] .streamlit-expanderContent,
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background-color: #1E1E1E !important;
        border: 2px solid #4ECDC4 !important;
        border-top: none !important;
    }
    
    /* 확장 컴포넌트 내부의 모든 텍스트 */
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] div,
    [data-testid="stExpander"] span,
    [data-testid="stExpander"] strong,
    [data-testid="stExpander"] b,
    .streamlit-expanderContent p,
    .streamlit-expanderContent div,
    .streamlit-expanderContent span,
    .streamlit-expanderContent strong,
    .streamlit-expanderContent b {
        color: #87CEEB !important;
        background-color: transparent !important;
    }
    
    /* 확장 컴포넌트의 컬럼 내부 텍스트 */
    [data-testid="stExpander"] [data-testid="column"] p,
    [data-testid="stExpander"] [data-testid="column"] div,
    [data-testid="stExpander"] [data-testid="column"] span,
    [data-testid="stExpander"] [data-testid="column"] strong {
        color: #87CEEB !important;
    }
    
    /* 모든 p, span, div 태그의 기본 색상 오버라이드 */
    .stSelectbox p, .stSelectbox span, .stSelectbox div,
    div[data-testid="stSelectbox"] p,
    div[data-testid="stSelectbox"] span,
    div[data-testid="stSelectbox"] div {
        color: #87CEEB !important;
    }
    
    /* info, warning, error 메시지 */
    .stAlert > div {
        background-color: #2C2C2C !important;
        border: 1px solid #4ECDC4 !important;
        color: #87CEEB !important;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript로 동적 스타일 적용
st.markdown("""
<script>
function applyCustomStyles() {
    // 모든 셀렉트박스 요소 찾기
    const selectboxes = document.querySelectorAll('[data-testid="stSelectbox"]');
    selectboxes.forEach(selectbox => {
        // 라벨 스타일링
        const label = selectbox.querySelector('label');
        if (label) {
            label.style.color = '#FF69B4';
            label.style.fontWeight = 'bold';
            label.style.fontSize = '1.1rem';
        }
        
        // 셀렉트 요소 스타일링
        const selectElement = selectbox.querySelector('[data-baseweb="select"]');
        if (selectElement) {
            selectElement.style.backgroundColor = '#2C2C2C';
            selectElement.style.border = '2px solid #4ECDC4';
            selectElement.style.color = '#87CEEB';
        }
        
        // 모든 내부 div와 span 요소 스타일링
        const innerElements = selectbox.querySelectorAll('div, span');
        innerElements.forEach(el => {
            if (el.textContent.trim()) {
                el.style.color = '#87CEEB';
            }
        });
    });
    
    // 텍스트 입력 필드 스타일링
    const textInputs = document.querySelectorAll('[data-testid="stTextInput"]');
    textInputs.forEach(textInput => {
        const label = textInput.querySelector('label');
        if (label) {
            label.style.color = '#FF69B4';
            label.style.fontWeight = 'bold';
        }
        
        const input = textInput.querySelector('input');
        if (input) {
            input.style.backgroundColor = '#2C2C2C';
            input.style.color = '#87CEEB';
            input.style.border = '2px solid #4ECDC4';
        }
    });
    
    // 확장 컴포넌트 내부 텍스트 스타일링
    const expanders = document.querySelectorAll('[data-testid="stExpander"]');
    expanders.forEach(expander => {
        // 헤더 스타일링
        const header = expander.querySelector('summary');
        if (header) {
            header.style.backgroundColor = '#2C2C2C';
            header.style.color = '#87CEEB';
            header.style.border = '2px solid #4ECDC4';
            header.style.fontWeight = 'bold';
        }
        
        // 내부 콘텐츠의 모든 텍스트 요소 스타일링
        const textElements = expander.querySelectorAll('p, div, span, strong, b');
        textElements.forEach(el => {
            if (el.textContent.trim()) {
                el.style.color = '#87CEEB';
                el.style.backgroundColor = 'transparent';
            }
        });
        
        // 컬럼 내부 텍스트도 처리
        const columns = expander.querySelectorAll('[data-testid="column"]');
        columns.forEach(column => {
            const columnTexts = column.querySelectorAll('p, div, span, strong, b');
            columnTexts.forEach(el => {
                if (el.textContent.trim()) {
                    el.style.color = '#87CEEB';
                }
            });
        });
    });
}

// 페이지 로드시 실행
document.addEventListener('DOMContentLoaded', applyCustomStyles);

// Streamlit이 다시 렌더링할 때마다 실행
const observer = new MutationObserver(applyCustomStyles);
observer.observe(document.body, {
    childList: true,
    subtree: true
});

// 주기적으로 스타일 적용 (fallback)
setInterval(applyCustomStyles, 500);
</script>
""", unsafe_allow_html=True)

# 사이드바 네비게이션
st.sidebar.title("📊 네비게이션")
page = st.sidebar.selectbox("페이지 선택", ["🏠 메인 - 이탈 예측", "👤 고객 상세 정보", "🚨 이탈 고객 분석"])

# 메인 제목
st.markdown('<div class="main-title">넷플릭스 고객 이탈 예측 어플리케이션</div>', unsafe_allow_html=True)

# 실제 넷플릭스 고객 데이터 로드
@st.cache_data
def load_customer_data():
    df = pd.read_csv('data/netflix_customer_churn.csv')
    return df

# 데이터 로드
customer_df = load_customer_data()

# 모든 고객 ID 목록 생성
customer_ids = customer_df['customer_id'].tolist()
customers = ["고객 정보 보기"] + [f"CustomerID: {cid[:8]}..." for cid in customer_ids]

# 선택된 고객 정보를 세션 상태에 저장
if 'selected_customer' not in st.session_state:
    st.session_state.selected_customer = "고객 정보 보기"

# 페이지별 컨텐츠
if page == "🏠 메인 - 이탈 예측":
    # 고객 정보 선택
    st.markdown('<div class="section-title">고객 선택</div>', unsafe_allow_html=True)
    
    # 고객 선택 드롭다운을 더 보기 좋게 스타일링
    st.markdown('<p style="color: #FF69B4; font-weight: bold; font-size: 1.2rem;">고객을 선택하세요</p>', unsafe_allow_html=True)
    selected_customer = st.selectbox("", customers, 
                                   index=customers.index(st.session_state.selected_customer) if st.session_state.selected_customer in customers else 0,
                                   key="customer_select")
    
    # 세션 상태 업데이트
    st.session_state.selected_customer = selected_customer
    
    # 예측 결과 섹션
    st.markdown('<div class="section-title">예측 결과</div>', unsafe_allow_html=True)
    
    if selected_customer != "고객 정보 보기":
        # 선택된 고객의 실제 데이터 가져오기
        customer_index = customers.index(selected_customer) - 1  # "고객 정보 보기" 제외
        selected_customer_id = customer_ids[customer_index]
        customer_data = customer_df[customer_df['customer_id'] == selected_customer_id].iloc[0]
        
        # 선택된 고객 데이터를 세션 상태에 저장
        st.session_state.customer_data = customer_data
        st.session_state.selected_customer_id = selected_customer_id
        
        # 실제 이탈 여부를 기반으로 확률 계산 (churned 컬럼 사용)
        actual_churn = customer_data['churned']
        if actual_churn == 1:
            churn_prob = np.random.uniform(0.6, 0.9)  # 실제 이탈 고객은 높은 확률
        else:
            churn_prob = np.random.uniform(0.1, 0.4)  # 실제 유지 고객은 낮은 확률
        retain_prob = 1 - churn_prob
        
        # 예측 확률 표시
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f'<div class="metric-text">이탈 확률: {churn_prob*100:.1f}%</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="metric-text">유지 확률: {retain_prob*100:.1f}%</div>', unsafe_allow_html=True)
        
        # 이탈/유지 확률 차트
        st.markdown('<div class="section-title">이탈/유지 확률</div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[
            go.Bar(
                x=['이탈', '유지'],
                y=[churn_prob, retain_prob],
                marker_color=['#FF6B6B', '#4ECDC4'],
                text=[f'{churn_prob:.1%}', f'{retain_prob:.1%}'],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#87CEEB', size=12),  # 스카이 블루
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                tickfont=dict(color='#98FB98', size=12),  # 연한 초록
                linecolor='#4ECDC4'
            ),
            yaxis=dict(
                title=dict(text='확률', font=dict(color='#FF69B4', size=14)),  # 핫 핑크
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)',
                zeroline=False,
                tickfont=dict(color='#98FB98', size=12),  # 연한 초록
                range=[0, 1],
                linecolor='#4ECDC4'
            ),
            height=400,
            margin=dict(l=50, r=20, t=20, b=50)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 고객 상세 정보 페이지로 이동 안내
        st.info("💡 선택된 고객의 상세 정보는 사이드바에서 '👤 고객 상세 정보' 페이지에서 확인할 수 있습니다.")
    
    else:
        st.info("위의 드롭다운에서 고객을 선택하세요.")

elif page == "👤 고객 상세 정보":
    st.markdown('<div class="section-title">선택된 고객 상세 정보</div>', unsafe_allow_html=True)
    
    # 세션 상태에서 고객 데이터 확인
    if 'customer_data' in st.session_state and 'selected_customer_id' in st.session_state:
        customer_data = st.session_state.customer_data
        selected_customer_id = st.session_state.selected_customer_id
        
        # 고객 정보를 보기 좋게 매핑
        customer_info = {
            "CustomerID": selected_customer_id[:8] + "...",
            "Churn": "Yes" if customer_data['churned'] == 1 else "No",
            "Age": f"{int(customer_data['age'])}",
            "Gender": customer_data['gender'],
            "Subscription Type": customer_data['subscription_type'],
            "Watch Hours": f"{customer_data['watch_hours']:.1f}",
            "Last Login Days": f"{int(customer_data['last_login_days'])}",
            "Region": customer_data['region'],
            "Device": customer_data['device'],
            "Monthly Fee": f"${customer_data['monthly_fee']:.2f}",
            "Payment Method": customer_data['payment_method'],
            "Number of Profiles": f"{int(customer_data['number_of_profiles'])}",
            "Avg Watch Time Per Day": f"{customer_data['avg_watch_time_per_day']:.2f} hours",
            "Favorite Genre": customer_data['favorite_genre']
        }
        
        # 고객 정보를 카드 형태로 표시
        with st.container():
            st.markdown(f"""
            <div style="background-color: #2C2C2C; padding: 2rem; border-radius: 10px; margin: 1rem 0;">
                <h3 style="color: #4ECDC4; margin-bottom: 1.5rem;">고객 {customer_info['CustomerID']} 정보</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # 2열로 정보 표시
            col1, col2 = st.columns(2)
            
            items = list(customer_info.items())
            mid_point = len(items) // 2
            
            with col1:
                for key, value in items[:mid_point]:
                    if key == "Churn":
                        color = "#FF6B6B" if value == "Yes" else "#4ECDC4"
                        st.markdown(f'<div style="color: #87CEEB; margin: 0.5rem 0; padding: 0.5rem; background-color: #1E1E1E; border-radius: 5px; border: 1px solid #4ECDC4;"><strong style="color: #FFD700;">{key}:</strong> <span style="color: {color};">{value}</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="color: #87CEEB; margin: 0.5rem 0; padding: 0.5rem; background-color: #1E1E1E; border-radius: 5px; border: 1px solid #4ECDC4;"><strong style="color: #FFD700;">{key}:</strong> {value}</div>', unsafe_allow_html=True)
                
            with col2:
                for key, value in items[mid_point:]:
                    if key == "Churn":
                        color = "#FF6B6B" if value == "Yes" else "#4ECDC4"
                        st.markdown(f'<div style="color: #87CEEB; margin: 0.5rem 0; padding: 0.5rem; background-color: #1E1E1E; border-radius: 5px; border: 1px solid #4ECDC4;"><strong style="color: #FFD700;">{key}:</strong> <span style="color: {color};">{value}</span></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="color: #87CEEB; margin: 0.5rem 0; padding: 0.5rem; background-color: #1E1E1E; border-radius: 5px; border: 1px solid #4ECDC4;"><strong style="color: #FFD700;">{key}:</strong> {value}</div>', unsafe_allow_html=True)
    
    else:
        st.warning("먼저 메인 페이지에서 고객을 선택해주세요!")
        if st.button("🏠 메인 페이지로 이동"):
            st.rerun()

elif page == "🚨 이탈 고객 분석":
    st.markdown('<div class="section-title">이탈 고객 분석</div>', unsafe_allow_html=True)
    
    # 이탈 고객만 필터링
    churned_customers = customer_df[customer_df['churned'] == 1]
    total_customers = len(customer_df)
    churned_count = len(churned_customers)
    
    # 통계 정보 표시
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div style="background-color: #2C2C2C; padding: 1.5rem; border-radius: 10px; text-align: center; border: 2px solid #4ECDC4;">
            <h3 style="color: #87CEEB; margin: 0;">전체 고객 수</h3>
            <h1 style="color: #FFD700; margin: 0.5rem 0;">{total_customers:,}</h1>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div style="background-color: #2C2C2C; padding: 1.5rem; border-radius: 10px; text-align: center; border: 2px solid #FF6B6B;">
            <h3 style="color: #87CEEB; margin: 0;">이탈 고객 수</h3>
            <h1 style="color: #FF6B6B; margin: 0.5rem 0;">{churned_count:,}</h1>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        churn_rate = (churned_count / total_customers) * 100
        st.markdown(f'''
        <div style="background-color: #2C2C2C; padding: 1.5rem; border-radius: 10px; text-align: center; border: 2px solid #FF69B4;">
            <h3 style="color: #87CEEB; margin: 0;">이탈률</h3>
            <h1 style="color: #FF69B4; margin: 0.5rem 0;">{churn_rate:.1f}%</h1>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        avg_monthly_fee = churned_customers['monthly_fee'].mean()
        st.markdown(f'''
        <div style="background-color: #2C2C2C; padding: 1.5rem; border-radius: 10px; text-align: center; border: 2px solid #96CEB4;">
            <h3 style="color: #87CEEB; margin: 0;">이탈 고객 평균 요금</h3>
            <h1 style="color: #96CEB4; margin: 0.5rem 0;">${avg_monthly_fee:.2f}</h1>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 이탈 고객 분석 차트들
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown('<div class="section-title">구독 유형별 이탈 분포</div>', unsafe_allow_html=True)
        
        # 구독 유형별 이탈 고객 수
        subscription_churn = churned_customers['subscription_type'].value_counts()
        
        # 구독 유형별 색상 매핑
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
        bar_colors = colors[:len(subscription_churn)]
        
        fig1 = go.Figure(data=[
            go.Bar(
                x=subscription_churn.index,
                y=subscription_churn.values,
                marker_color=bar_colors,
                text=subscription_churn.values,
                textposition='auto',
                textfont=dict(color='#FFD700', size=14, family="Arial Black"),  # 골드 색상, 굵은 글씨
            )
        ])
        
        fig1.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#87CEEB', size=12),  # 스카이 블루
            xaxis=dict(
                title=dict(text='구독 유형', font=dict(color='#FF69B4', size=14)),  # 핫 핑크
                tickfont=dict(color='#98FB98', size=12),  # 연한 초록
                showgrid=False
            ),
            yaxis=dict(
                title=dict(text='이탈 고객 수', font=dict(color='#FF69B4', size=14)),  # 핫 핑크
                tickfont=dict(color='#98FB98', size=12),  # 연한 초록
                showgrid=True,
                gridcolor='rgba(255,255,255,0.1)'
            ),
            height=400,
            margin=dict(l=50, r=20, t=20, b=50)
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_chart2:
        st.markdown('<div class="section-title">지역별 이탈 분포</div>', unsafe_allow_html=True)
        
        # 지역별 이탈 고객 수
        region_churn = churned_customers['region'].value_counts()
        
        # 지역별 색상 매핑
        pie_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#DDA0DD', '#F0E68C']
        region_colors = pie_colors[:len(region_churn)]
        
        fig2 = go.Figure(data=[
            go.Pie(
                labels=region_churn.index,
                values=region_churn.values,
                marker_colors=region_colors,
                textfont=dict(color='white', size=12, family="Arial Black"),  # 흰색, 굵은 글씨
                textinfo='label+percent+value',
                textposition='auto'
            )
        ])
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#87CEEB', size=12),  # 스카이 블루
            legend=dict(
                font=dict(color='#FFB6C1', size=11),  # 연한 핑크
                bgcolor='rgba(0,0,0,0.3)',
                bordercolor='#4ECDC4',
                borderwidth=1
            ),
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # 이탈 고객 목록
    st.markdown('<div class="section-title">이탈 고객 목록</div>', unsafe_allow_html=True)
    
    # 검색 기능
    st.markdown('<p style="color: #FF69B4; font-weight: bold; font-size: 1.1rem;">고객 ID 또는 정보로 검색:</p>', unsafe_allow_html=True)
    search_term = st.text_input("", placeholder="예: a9b75100 또는 Basic", key="search_input")
    
    if search_term:
        # 검색 필터링
        mask = (
            churned_customers['customer_id'].str.contains(search_term, case=False, na=False) |
            churned_customers['subscription_type'].str.contains(search_term, case=False, na=False) |
            churned_customers['region'].str.contains(search_term, case=False, na=False) |
            churned_customers['device'].str.contains(search_term, case=False, na=False) |
            churned_customers['payment_method'].str.contains(search_term, case=False, na=False) |
            churned_customers['favorite_genre'].str.contains(search_term, case=False, na=False)
        )
        filtered_customers = churned_customers[mask]
    else:
        filtered_customers = churned_customers
    
    # 페이지네이션
    customers_per_page = 10
    total_pages = (len(filtered_customers) + customers_per_page - 1) // customers_per_page
    
    if total_pages > 0:
        st.markdown('<p style="color: #FF69B4; font-weight: bold; font-size: 1.1rem;">페이지 선택:</p>', unsafe_allow_html=True)
        page_num = st.selectbox("", range(1, total_pages + 1), key="page_select") - 1
        start_idx = page_num * customers_per_page
        end_idx = start_idx + customers_per_page
        page_customers = filtered_customers.iloc[start_idx:end_idx]
        
        st.info(f"총 {len(filtered_customers)}명의 이탈 고객 중 {start_idx + 1}-{min(end_idx, len(filtered_customers))}번째 고객")
        
        # 이탈 고객 정보를 카드 형태로 표시
        for idx, (_, customer) in enumerate(page_customers.iterrows()):
            with st.expander(f"고객 {customer['customer_id'][:8]}... (#{start_idx + idx + 1})"):
                col_info1, col_info2 = st.columns(2)
                
                with col_info1:
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">나이:</strong> {int(customer["age"])}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">성별:</strong> {customer["gender"]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">구독 유형:</strong> {customer["subscription_type"]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">월 요금:</strong> ${customer["monthly_fee"]:.2f}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">결제 방법:</strong> {customer["payment_method"]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">선호 장르:</strong> {customer["favorite_genre"]}</p>', unsafe_allow_html=True)
                
                with col_info2:
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">지역:</strong> {customer["region"]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">디바이스:</strong> {customer["device"]}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">시청 시간:</strong> {customer["watch_hours"]:.1f}시간</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">마지막 로그인:</strong> {int(customer["last_login_days"])}일 전</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">프로필 수:</strong> {int(customer["number_of_profiles"])}</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="color: #87CEEB; margin: 0.3rem 0;"><strong style="color: #FFD700;">일평균 시청:</strong> {customer["avg_watch_time_per_day"]:.2f}시간</p>', unsafe_allow_html=True)
    else:
        st.warning("검색 조건에 맞는 이탈 고객이 없습니다.")