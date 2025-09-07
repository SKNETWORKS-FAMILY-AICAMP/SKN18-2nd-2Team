import streamlit as st
import base64
from streamlit_card import card
from sidebar_utils import *

#####################
# 메인페이지 만들기 #
#####################

def after_login():
    # 넷플릭스 프로필 설정
    profiles = [
        {"name": "안시현", "avatar": "https://i.pinimg.com/474x/e3/94/30/e39430434d2b8207188f880ac66c6411.jpg", "info": "팀장 팀장님"},
        {"name": "김규리", "avatar": "https://i.pinimg.com/564x/1b/a2/e6/1ba2e6d1d4874546c70c91f1024e17fb.jpg", "info": "진짜 팀장님"},
        {"name": "김민주", "avatar": "https://wallpapers.com/images/hd/netflix-profile-pictures-1000-x-1000-dyrp6bw6adbulg5b.jpg", "info": "진짜 진짜 팀장님"},
        {"name": "김주석", "avatar": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Netflix-avatar.png", "info": "최종 팀장님"},
        {"name": "최준호", "avatar": "https://wallpapers.com/images/hd/netflix-profile-pictures-1000-x-1000-88wkdmjrorckekha.jpg", "info": "최최종 팀장님"},
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


# --- AUTOPLAY THE AUDIO ---
def autoplay_audio(file_path: str):
    # app를 실행했을 때 넷플릭스 효과음 재생
    # 자동 실행시키기 위해서 소리허용 설정 필요
    audio_file = open('./images/audio_netflix.mp3', 'rb')
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
    setup_css_styles(), set_page(), login_button(), after_login(), autoplay_audio("./images/audio_netflix.mp3"), set_sidebar(), ad(), 
