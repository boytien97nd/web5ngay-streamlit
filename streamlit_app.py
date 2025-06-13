import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from gtts import gTTS
from moviepy.editor import *
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🎬 Tạo Video Phong Cách Web5ngay từ YouTube")
st.markdown("Chỉ cần dán link video Mark Tilbury, hệ thống sẽ tự động tạo giọng + dựng video bằng tiếng Việt")

video_url = st.text_input("Nhập link video YouTube:")
run_button = st.button("Tạo Video")

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

def create_video(voice_file, output_file="output.mp4"):
    bg = ColorClip(size=(1280, 720), color=(10,10,10), duration=60)
    audio = AudioFileClip(voice_file)
    video = bg.set_audio(audio).set_duration(audio.duration)
    video.write_videofile(output_file, fps=24)
    return output_file

if run_button and video_url:
    try:
        video_id = video_url.split("v=")[-1].split("&")[0]
        with st.spinner("Đang lấy transcript..."):
            raw_text = get_transcript(video_id)

        with st.spinner("Đang chuyển thể sang phong cách Web5ngay..."):
            viet_text = rewrite_script(raw_text)
            st.text_area("Kịch bản tiếng Việt:", viet_text, height=250)

        with st.spinner("Đang tạo giọng đọc..."):
            voice_path = generate_voice(viet_text)

        with st.spinner("Đang dựng video..."):
            video_path = create_video(voice_path)

        st.success("🎉 Hoàn tất! Tải video bên dưới")
        st.video(video_path)
        with open(video_path, "rb") as f:
            st.download_button("📥 Tải video", f, file_name="video_web5ngay.mp4")

    except Exception as e:
        st.error(f"Lỗi: {e}")
