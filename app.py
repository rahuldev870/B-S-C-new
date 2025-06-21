import streamlit as st
import requests
import base64

st.set_page_config(page_title="Braille to Speech Converter", layout="centered")

st.title("🟦 Braille to Speech Converter")
st.markdown("Upload a Braille image, convert it to text, and listen to the audio output.")

uploaded_file = st.file_uploader("Upload Braille Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if st.button("Convert to Text"):
        with st.spinner("Processing image..."):
            files = {"file": uploaded_file.getvalue()}
            res = requests.post("https://bsc-backend.onrender.com/digest", files={"file": uploaded_file})
            
            if res.ok:
                data = res.json()
                if data.get("error"):
                    st.error(data["message"])
                else:
                    st.success("Text extracted successfully!")
                    st.text_area("Braille Output Text", data["digest"], height=150, key="output_text")
                    output_text = data["digest"]

                    if st.button("🔊 Play Text"):
                        tts_res = requests.post("https://bsc-backend.onrender.com/speech", data={"text": output_text})
                        if tts_res.ok:
                            audio_url = tts_res.json()["url"]
                            final_url = f"https://bsc-backend.onrender.com{audio_url}"

                            st.markdown(
                                f"""
                                <audio controls autoplay>
                                  <source src="{final_url}" type="audio/mpeg">
                                  Your browser does not support the audio element.
                                </audio>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.error("Failed to generate audio.")
            else:
                st.error("Failed to upload/process image.")
