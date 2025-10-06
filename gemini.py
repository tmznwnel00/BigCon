import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = API_KEY

def generate_text(prompt: str, model: str = "gemini-2.5-flash") -> str:
    chat = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=API_KEY,
        temperature=0.1
    )
    response = chat.invoke(prompt)
    return response.content

st.title("Gemini 2.5 Flash Demo")
prompt = st.text_area("프롬프트를 입력하세요:")

if st.button("생성"):
    if prompt.strip():
        with st.spinner("생성 중..."):
            result = generate_text(prompt)
        st.success("응답:")
        st.write(result)
    else:
        st.warning("프롬프트를 입력하세요.")