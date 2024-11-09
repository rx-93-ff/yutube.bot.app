from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re  # 정규식 모듈 추가

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("GOOGLE_API_KEY")

# API 키 설정
genai.configure(api_key=api_key)

st.set_page_config(page_title="Youtube Summarizer", page_icon="📺")

st.header("My Youtube Summarizer Web Application")

youtube_link = st.text_input("Enter Youtube Video Link")

# video_id를 추출하는 함수
def extract_video_id(link):
    try:
        # youtube.com 링크에서 video_id 추출
        if "youtube.com" in link:
            return link.split("v=")[1].split("&")[0]
        # youtu.be 링크에서 video_id 추출
        elif "youtu.be" in link:
            return link.split("/")[-1]
        else:
            raise ValueError("Invalid URL format")
    except Exception as e:
        raise ValueError("Invalid URL format")

if youtube_link:
    try:
        video_id = extract_video_id(youtube_link)
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except Exception as e:
        st.write("Invalid URL")

submit = st.button("Summarize")

prompt = """You are a YouTube video summarizer. You will take the transcript text and summarize the
entire video, providing the important summary. Please provide the summary of the text given here in two
languages, English and Hindi within 250-300 words. Please translate accordingly.\n\n"""

def extract_transcript_details(video_url):
    try:
        video_id = extract_video_id(video_url)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "ko"])
        transcript = ""
        for i in transcript_text:
            transcript += " " + i['text']
        return transcript
    except Exception as e:
        raise e

if submit:
    try:
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            model = genai.GenerativeModel("gemini-pro")
            summary = model.generate_content(prompt + transcript_text)
            st.write(summary.text)
        else:
            st.write("Unable to summarize")
    except Exception as e:
        st.write("Unable to summarize")
