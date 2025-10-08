import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

API_KEY = st.secrets["GOOGLE_API_KEY"]
os.environ["GOOGLE_API_KEY"] = API_KEY

# MultiServerMCPClient 생성
client = MultiServerMCPClient(
    {
        "firebase": {
            "url": "http://127.0.0.1:8000/sse",
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