import os
import subprocess
import streamlit as st
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

API_KEY = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = API_KEY


# @st.cache_resource
# def start_mcp_server():
#     import requests

#     # MCP 서버가 이미 실행 중인지 확인
#     try:
#         requests.get("http://127.0.0.1:8000/sse", timeout=2)
#         print("✅ Firebase MCP server already running.")
#         return None
#     except Exception:
#         print("🚀 Starting Firebase MCP server...")
#         process = subprocess.Popen(
#             ["uv", "run", "servers/firebase_mcp.py"],  
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#         )

#         # 서버 준비될 때까지 헬스체크
#         for _ in range(10):
#             try:
#                 time.sleep(1)
#                 requests.get("http://127.0.0.1:8000/sse", timeout=2)
#                 print("✅ Firebase MCP server is ready.")
#                 return process
#             except Exception:
#                 continue
#         print("⚠️ MCP server not responding after 10 seconds.")
#         return process

# mcp_process = start_mcp_server()

# MultiServerMCPClient 생성
client = MultiServerMCPClient(
    {
        "firebase": {
            # "url": "http://bigcon-production.up.railway.app/mcp",
            # "transport": "streamable_http",
            "url": "http://bigcon-production.up.railway.app/sse",
            "transport": "sse",
        },
        # 필요하면 다른 MCP 서버 추가
    }
)

# tools 가져오기
tools = asyncio.run(client.get_tools())  # list of all tools


# 에이전트 생성
chat = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=API_KEY,
    temperature=0.1
)

# 에이전트 생성
agent = initialize_agent(
    tools=tools,
    llm=chat,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

async def async_agent_run(prompt):
    return await agent.arun(prompt)

# Streamlit UI
st.title("Gemini 2.5 Flash + MultiServer MCP Demo")
prompt = st.text_area("프롬프트를 입력하세요:")

if st.button("생성"):
    if prompt.strip():
        with st.spinner("생성 중..."):
            result = asyncio.run(async_agent_run(prompt))
        st.success("응답:")
        st.write(result)
    else:
        st.warning("프롬프트를 입력하세요.")