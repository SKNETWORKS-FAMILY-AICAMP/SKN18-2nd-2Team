import streamlit as st
import base64

#####################
# 메인페이지 만들기 #
#####################


# 최상단에 netflix 로고 이미지 삽입
st.image("Logonetflix.png", width=1500) 
st.title("˙⋆✮🎥고객 이탈 예측 서비스🍿✮⋆˙")

centered_text = """
<div style="text-align: center;">
🔎이 서비스는 고객 데이터를 기반으로 이탈 확률을 예측하고<br>
🪄이탈 가능성이 높은 고객에게 맞춤 프로모션을 추천하며<br>
📊고객별 이탈 사유를 분석해 시각화합니다.
</div>
"""
st.markdown(centered_text, unsafe_allow_html=True)



# app를 실행했을 때 넷플릭스 효과음 재생
# 자동 실행시키기 위해서 소리허용 설정 필요
audio_file = open('audio_netflix.mp3', 'rb')
st.audio(audio_file.read(), format='audio/mp3')

# --- HIDE THE AUDIO PLAYER UI ---
# Use CSS to make the audio player invisible
hide_player_css = """
<style>
    audio {
        display: none;
    }
</style>
"""
st.markdown(hide_player_css, unsafe_allow_html=True)


# --- AUTOPLAY THE AUDIO ---
def autoplay_audio(file_path: str):
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


# Call the function to autoplay the audio
autoplay_audio("audio_netflix.mp3")


#################
# Side Bar 설정 #
#################
# 각각의 페이지로 넘어가도록 연결하기
st.sidebar.title("🚀페이지 이동🚀")
st.sidebar.page_link("app.py", label="📍기본 페이지📍")
st.sidebar.page_link("pages/1 Prediction.py", label="🔎고객 이탈 확률 예측🔎")
st.sidebar.page_link("pages/2 Recommendations.py", label="🪄프로모션 추천🪄")
st.sidebar.success("🙋🏻버튼을 클릭하여 원하는 기능을 사용해보세요!💁🏻‍♀️")