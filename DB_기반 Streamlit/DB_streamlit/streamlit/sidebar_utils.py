import streamlit as st
from PIL import Image
import time

def setup_shared_sidebar():

    setup_css_styles()
    """모든 페이지에서 공통으로 사용하는 사이드바 설정"""
    # 세션 상태 초기화
    if 'login' not in st.session_state:
        st.session_state.login = False
    
    # 로그인/로그아웃 섹션
    handle_sidebar_login()
    
    # 페이지 네비게이션
    setup_sidebar_navigation()

    display_sidebar_ads()

def handle_sidebar_login():
    """사이드바 로그인/로그아웃 처리"""
    with st.sidebar:
        if st.session_state.login:
            st.header("코딩좋아 ㅎㅎ 님 반갑습니다.")
            if st.button("Logout", key="logout_btn"):
                st.session_state.login = False
                st.rerun()
        else:
            st.header("로그인이 필요합니다.")
            if st.button("Login", key="login_btn"):
                st.session_state.login = True
                st.rerun()

def setup_sidebar_navigation():
    """사이드바 네비게이션 설정"""
    st.sidebar.header("🚀페이지 이동🚀")
    st.sidebar.page_link("app.py", label="📍기본 페이지📍")
    st.sidebar.page_link("pages/1 Prediction.py", label="🔎고객 이탈 확률 예측🔎")
    st.sidebar.page_link("pages/2 Recommendations.py", label="🪄분석및 프로모션 추천🪄")
    st.sidebar.success("🙋🏻버튼을 클릭하여 원하는 기능을 사용해보세요!💁🏻‍♀️")   

def get_ad_list():
    """광고 리스트 데이터 반환"""
    return [
        {"image": "./images/말차라떼 머셔~.png", "text": "쌉사름하고 진한 말차의 향을 그대로!"},
        {"image": "./images/바나나라떼 머셔~.png", "text": "당 떨어질 땐? 밍그래 머셔~"},
        {"image": "./images/소주 머셔~.png", "text": "이모 청이슬 하나요."}
    ]

def display_sidebar_ads():
    """사이드바 광고 표시"""
    ad_list = get_ad_list()
    st.sidebar.subheader("광고문의: 02-9965-4668")
    with st.sidebar:
        image_placeholder = st.empty()
    
    current_index = 0
    
    while True:
        if ad_list:
            try:
                current_ad = ad_list[current_index]
                image = Image.open(current_ad["image"])
                
                with image_placeholder.container():
                    st.write(f"**{current_ad['text']}**")
                    st.image(image, width='stretch')
                
                current_index = (current_index + 1) % len(ad_list)
            except:
                pass
        
        time.sleep(2)

def setup_css_styles():
    """CSS 스타일 설정"""
    st.markdown("""
    <style>
        /* 전체 배경을 어둡게 설정 */
        .main {
            background-color: #141414;
            color: white;
        }
        /* 프로필 선택 제목 스타일 */
        h1 {
            text-align: center;
            color: white;
            font-weight: bold;
        }
        /* 프로필 관리 버튼 스타일 */
        .stButton>button {
            display: block;
            margin: 0 auto;
            border: 1px solid white;
            background-color: transparent;
            color: grey;
            padding: 10px 20px;
            border-radius: 0;
            font-size: 16px;
        }
        .stButton>button:hover {
            border-color: white;
            color: white;
        }
        
        /* 사이드바 배경색 설정 */
        [data-testid="stSidebar"] {
            background-color: #0E1117;
        }

        /* 메인 바탕화면 배경색 설정 */
        .main {
            background-color: #0E1117;
        }
        
        /* 기본 sidebar 없애기 */
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebarNav"] {display: none;}
        
        /* 오디오 플레이어 숨기기 */
        audio {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)