import streamlit as st
import base64
import time
from PIL import Image
from streamlit_card import card
from sidebar_utils import setup_shared_sidebar

#####################
# 메인페이지 만들기 #
#####################


# --- 페이지 설정 ---
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



def after_login():
    # 넷플릭스 프로필 설정
    profiles = [
        {"name": "안시현", "avatar": "https://i.pinimg.com/474x/e3/94/30/e39430434d2b8207188f880ac66c6411.jpg", "info": "팀장님"},
        {"name": "김규리", "avatar": "https://i.pinimg.com/564x/1b/a2/e6/1ba2e6d1d4874546c70c91f1024e17fb.jpg", "info": "팀장님"},
        {"name": "김민주", "avatar": "https://wallpapers.com/images/hd/netflix-profile-pictures-1000-x-1000-dyrp6bw6adbulg5b.jpg", "info": "팀장님"},
        {"name": "김주석", "avatar": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Netflix-avatar.png", "info": "팀장님"},
        {"name": "최준호", "avatar": "https://wallpapers.com/images/hd/netflix-profile-pictures-1000-x-1000-88wkdmjrorckekha.jpg", "info": "팀장님"},
    ]
    # 로그인 상태일 경우 프로필 선택 창이 나타남
    if st.session_state.login:
        
        st.subheader("예측 서비스를 이용할 프로필을 선택하세요.")
        st.write("")
        st.write("")

        cols = st.columns(len(profiles))

        for i, profile in enumerate(profiles):
            with cols[i]:
                clicked = card(
                    title=profile["name"],
                    text="",
                    image=profile["avatar"],
                    styles={
                        "card": {
                            "width": "130px",
                            "height": "130px",
                            "border-radius": "8px",
                            "margin": "0 auto",
                            "background-color": "#E50914"
                        },
                        "image": { "object-fit": "cover", "height": "100%" }
                    },
                    on_click=lambda: st.info(profile["info"]) 
                )

        st.write("")
        st.write("")
        st.button("프로필 관리")

    else:
        # --- 5. 로그인이 False일 때 안내 메시지를 보여줌 ---
        st.warning("서비스를 이용하려면 사이드바에서 먼저 로그인해주세요.")



# 광고창 
def ad():
    ad_list = [
        {"image": "./images/말차라떼 머셔~.png", "text": "쌉사름하고 진한 말차의 향을 그대로!"},
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


def set_sidebar():
    # 기본 sidebar 없애기
    st.markdown("""
        <style>
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebarNav"] {display: none;}
        </style>
        """, unsafe_allow_html=True)

    #################
    # Side Bar 설정 #
    #################
    st.sidebar.header("🚀페이지 이동🚀")
    st.sidebar.page_link("app.py", label="📍기본 페이지📍")
    st.sidebar.page_link("pages/1 Prediction.py", label="🔎고객 이탈 확률 예측🔎")
    st.sidebar.page_link("pages/2 Recommendations.py", label="🪄분석및 프로모션 추천🪄")
    st.sidebar.success("🙋🏻버튼을 클릭하여 원하는 기능을 사용해보세요!💁🏻‍♀️")   



# --- AUTOPLAY THE AUDIO ---
def autoplay_audio(file_path: str):
    # app를 실행했을 때 넷플릭스 효과음 재생
    # 자동 실행시키기 위해서 소리허용 설정 필요
    audio_file = open('audio_netflix.mp3', 'rb')
    st.audio(audio_file.read(), format='audio/mp3')

    # 창에 떠있는 오디오플레이어 숨기기
    hide_player_css = """
    <style>
        audio {
            display: none;
        }
    </style>
    """
    st.markdown(hide_player_css, unsafe_allow_html=True)

    # Read the audio file from the local file system
    with open(file_path, "rb") as f:
        data = f.read()
    
    # Encode the audio data to Base64
    b64 = base64.b64encode(data).decode()
    
    # Create the HTML audio tag with autoplay
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    # Embed the HTML into the Streamlit app
    st.components.v1.html(md, height=0)




if __name__ == "__main__":
    st.session_state["current_page"] = "app"
    set_page(), login_button(), after_login(), set_sidebar(), ad(), autoplay_audio("audio_netflix.mp3"),setup_shared_sidebar()
