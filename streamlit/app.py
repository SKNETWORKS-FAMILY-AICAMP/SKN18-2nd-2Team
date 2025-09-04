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
st.write("")
st.write("")
st.write("")




# 기본 sidebar 없애기
st.markdown("""
    <style>
    footer {visibility: hidden;}
    [data-testid="stMainMenu"] {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


# sidebar에 각각의 페이지로 넘어가도록 연결하기
st.sidebar.header("🚀페이지 이동🚀")
st.sidebar.page_link("app.py", label="📍기본 페이지📍")
st.sidebar.page_link("pages/1 Prediction.py", label="🔎고객 이탈 확률 예측🔎")
st.sidebar.page_link("pages/2 Recommendations.py", label="🪄프로모션 추천🪄")
st.sidebar.page_link("pages/3 Reasons.py", label="📊이탈 사유 분석📊")
st.sidebar.success("🙋🏻버튼을 클릭하여 원하는 기능을 사용해보세요!💁🏻‍♀️")

# 지금 뜨는 콘텐츠
content_data = [
    {"img": "https://occ-0-988-325.1.nflxso.net/dnm/api/v6/mAcAr9TxZIVbINe88xb3Teg5_OA/AAAABQBYUL3Qpm0ZLhYDdmy2GUNsQBOPSLfduvgfWwxxRSzUlEL81tG9HwzUSL0y-4vdcDDl1hUKmd31OvOZHPDdjy9lbhpMIxgvHikM8056iSoEGxSOoEYCvqqX0wb23gxnz2Bu.webp?r=ff7", "title": "케이팝 데몬 헌터스"},
    {"img": "https://occ-0-988-325.1.nflxso.net/dnm/api/v6/mAcAr9TxZIVbINe88xb3Teg5_OA/AAAABR5J80TeGdGhsKAcYwKdzusc4_kifLk_yiSVrYKNC4RMt4n2Bkr136690q5kaQwOqHM9RZducCy7hqWP4RUPmnTC6QM39d6Ta0oFzK3Ln1Bx4C0cf3NQir9S4vmjB-pLzqxD.webp?r=05e", "title": "애마"},
    {"img": "https://occ-0-988-325.1.nflxso.net/dnm/api/v6/mAcAr9TxZIVbINe88xb3Teg5_OA/AAAABe6acOVBzNkmGSQvFspkyVWfbo1raPZkUhsH9_exmg26UAFAfjXPNkUAw4NTERSzA_E3CN6Z0oJLH2I_9vX_bBuxeohH0UuCjQu5AjyBPXIBa4HwVusgIhuK3XQ9Gs5NAFkO.webp?r=4b2", "title": "트리거"},
    {"img": "https://occ-0-988-325.1.nflxso.net/dnm/api/v6/mAcAr9TxZIVbINe88xb3Teg5_OA/AAAABVuAvVIHv5vvI0r939iO_TvF0XM0jbvfnUzZC4z1aTOGckTOHDdLxqk0NeWsffNtpXNcmIMQQT1uJnOey5dmtQz1yuNtLt9OmzQ.webp?r=7f4", "title": "폭군의 셰프"},
    {"img": "https://occ-0-988-325.1.nflxso.net/dnm/api/v6/mAcAr9TxZIVbINe88xb3Teg5_OA/AAAABUDIsOkh8w9Oyt2Ywuhp_3ReATSDDzyXcnCoLUeLK023NqIUcvu9r3qT9FAjxlaz5ew-J5c1gS1QwlxP84TVN8DBOjS6xhmU1as7s449deddH_w_bb8WC5ytfD-zMIg4Z3yR.webp?r=8d8", "title": "나는 생존자다"},
    {"img": "https://occ-0-988-325.1.nflxso.net/dnm/api/v6/mAcAr9TxZIVbINe88xb3Teg5_OA/AAAABcv94NKVHP5EqETcbS317GF0i4A-6Z0jfFWqaLdsnKzHrygXSYgbLAgYhOKWkPeGt3ertTWI0DAGKL4oKc5loLpea6sKB9MvFGTJstNmdpceLnMv7MeghyA22aNZsAEw54E0.webp?r=4ca", "title": "고백의 역사"},
    {"img": "https://occ-0-988-325.1.nflxso.net/dnm/api/v6/mAcAr9TxZIVbINe88xb3Teg5_OA/AAAABWTM77d-Us_-_iFkO9XPjG4WfAIUfrhobEsDDcTZ7Zs5WnsKMa4fN9DwTikl4gupBjm77GL8GhajKr4KD8UeMe4A3rwifeqkX8N9gIJFzEH6Rs6ClCjdQp4oRBxa2d3r_q1i.webp?r=3ab", "title": "폭싹 속았수다"},
]

st.header("지금 뜨는 콘텐츠")
cols = st.columns(7)

for i, item in enumerate(content_data):
    with cols[i]:
        st.image(item["img"])
        st.markdown(f"**{i+1}. {item['title']}**")






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