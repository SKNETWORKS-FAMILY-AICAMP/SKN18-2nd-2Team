import streamlit as st
from PIL import Image
import time


def set_page():
    # 최상단에 netflix 로고 이미지 삽입
    st.image(".\images\Logonetflix.png", width=2000) 
    st.title("˙⋆✮🎥고객 이탈 예측 서비스🍿✮⋆˙")

    centered_text = """
    <div style="text-align: center;">
    🔎이 서비스는 고객 데이터를 기반으로 이탈 확률을 예측하고<br>
    🪄이탈 가능성이 높은 고객에게 맞춤 프로모션을 추천하며<br>
    📊고객별 이탈 사유를 분석해 시각화합니다.
    </div>
    """
    st.markdown(centered_text, unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")

    st.set_page_config(
        page_title="Streamlit Netflix Profiles",
        layout="centered"
    )

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

def set_sidebar():
    st.sidebar.header("🚀페이지 이동🚀")
    st.sidebar.page_link("app.py", label="📍기본 페이지📍")
    st.sidebar.page_link("pages/1 Prediction.py", label="🔎고객 이탈 확률 예측🔎")
    st.sidebar.page_link("pages/2 Recommendations.py", label="🪄분석 및 프로모션 추천🪄")
    st.sidebar.success("🙋🏻버튼을 클릭하여 원하는 기능을 사용해보세요!💁🏻‍♀️")

# 광고창 
def ad():
    ad_list = [
        {"image": "./images/말차라떼 머셔~.png", "text": "진한 말차의 향을 그대로!"},
        {"image": "./images/바나나라떼 머셔~.png", "text": "당 떨어질 땐? 밍그래 머셔~"},
        {"image": "./images/소주 머셔~.png", "text": "이모 청이슬 하나요."}
]
    # 사이드바에 이미지 순차 출력
    with st.sidebar:
        image_placeholder = st.empty()
    
    # 이미지 순환
    current_index = 0
    st.sidebar.write("광고문의: 02-9965-4668")
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
        time.sleep(2)  # 2초마다 변경

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
        [data-testid="stSidebarNav"] {display: none;}
        
        /* 오디오 플레이어 숨기기 */
        audio {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

def login_button():
    # 기본값: 로그아웃
    if 'login' not in st.session_state:
        st.session_state.login = False

# 사이드바 로그인/로그아웃 
    with st.sidebar:
        if st.session_state.login:
            # 로그인이 된 경우
            st.header("코딩좋아 ㅎㅎ 님 반갑습니다.")
            if st.button("Logout"):
                st.session_state.login = False
                st.rerun() # 페이지 새로고침
        else:
            # 로그인이 안 된 경우
            st.header("로그인이 필요합니다.")
            if st.button("Login"):
                st.session_state.login = True
                st.rerun() # 페이지 새로고침