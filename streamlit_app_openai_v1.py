
import streamlit as st
import openai
from gtts import gTTS
import os

# Tạo client OpenAI (chuẩn phiên bản >=1.0.0)
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("🧠 Tạo Kịch Bản & Giọng Đọc Phong Cách Web5ngay")
st.markdown("Dán nội dung transcript tiếng Anh từ video YouTube (ví dụ Mark Tilbury), hệ thống sẽ tạo script Web5ngay và giọng đọc tiếng Việt")

input_text = st.text_area("📋 Dán nội dung transcript tiếng Anh vào đây:", height=300)
run_button = st.button("Tạo nội dung")

def rewrite_script(text):
    prompt = f"""
    Viết lại nội dung sau thành phong cách kể chuyện truyền cảm hứng như Web5ngay, bằng tiếng Việt, ngắn gọn, rõ ràng:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_voice(text, filename="voice.mp3"):
    tts = gTTS(text=text, lang='vi')
    tts.save(filename)
    return filename

if run_button and input_text:
    try:
        with st.spinner("✍️ Đang chuyển thể sang phong cách Web5ngay..."):
            viet_text = rewrite_script(input_text)
            st.text_area("📜 Kịch bản tiếng Việt:", viet_text, height=300)

        with st.spinner("🔊 Đang tạo giọng đọc..."):
            voice_path = generate_voice(viet_text)
            st.audio(voice_path)

        with open(voice_path, "rb") as f:
            st.download_button("📥 Tải file giọng đọc", f, file_name="web5ngay_voice.mp3")

    except Exception as e:
        st.error("❌ Có lỗi xảy ra khi xử lý nội dung. Hãy đảm bảo bạn đã dán transcript tiếng Anh hợp lệ và OpenAI API key của bạn vẫn hoạt động. Chi tiết lỗi:")
        st.code(str(e))
