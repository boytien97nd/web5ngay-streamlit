import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from gtts import gTTS
import os

# API key từ Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🧠 Tạo Kịch Bản & Giọng Đọc Phong Cách Web5ngay")
st.markdown("Từ link video YouTube (ví dụ Mark Tilbury), tạo kịch bản truyền cảm hứng + giọng đọc tiếng Việt")

video_url = st.text_input("Nhập link video YouTube:")
run_button = st.button("Tạo nội dung")

@st.cache_data
def get_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([item['text'] for item in transcript])
    return text

def rewrite_script(text):
    prompt = f"""
    Viết lại nội dung sau thành phong cách kể chuyện truyền cảm hứng như Web5ngay, bằng tiếng Việt, ngắn gọn, rõ ràng:
    {text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_voice(text, filename="voice.mp3"):
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)
    return filename

if run_button and video_url:
    try:
        video_id = video_url.split("v=")[-1].split("&")[0]
        with st.spinner("📄 Đang lấy transcript..."):
            raw_text = get_transcript(video_id)

        with st.spinner("✍️ Đang chuyển thể sang phong cách Web5ngay..."):
            viet_text = rewrite_script(raw_text)
            st.text_area("📜 Kịch bản tiếng Việt:", viet_text, height=300)

        with st.spinner("🔊 Đang tạo giọng đọc..."):
            voice_path = generate_voice(viet_text)
            st.audio(voice_path)

        with open(voice_path, "rb") as f:
            st.download_button("📥 Tải file giọng đọc", f, file_name="web5ngay_voice.mp3")

    except Exception as e:
        st.error(f"❌ Lỗi: {e}")
