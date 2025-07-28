from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

# llm = ChatVertexAI(model='gemini-2.5-flash', temperature=0, location='global')
llm = ChatGoogleGenerativeAI(
        # model="gemini-1.5-flash-latest", # 또는 "gemini-pro"
        model="gemini-2.0-flash",
        # model="gemini-2.5-flash-preview-04-17", # 안됨
        # client_options={"timeout": 60.0}, # LLM 호출 시 타임아웃 설정 (예: 60초)
        # streaming=True # 스트리밍을 사용하면 invoke의 결과 처리 방식이 달라질 수 있어 주의
)