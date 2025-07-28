from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver, MemorySaver
from dotenv import load_dotenv
import traceback
load_dotenv('.env')

import streamlit as st
from graph.workflow import graph_workflow
import config

user_id = "testuser1"

st.set_page_config(page_title="LangGraph Chatbot", page_icon="🤖")

# main_config = {**config.get_global_config(user_id, thread_id=None), **config.sub_configs.get("supervisor",{})}

st.title("LangGraph Chatbot (Streamlit UI)")

# 세션 상태에 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
if "config" not in st.session_state:
    st.session_state["config"] = {**config.get_global_config(thread_id=user_id), **config.sub_configs.get("supervisor",{})}

if "checkpoint" not in st.session_state:
    st.session_state["checkpoint"] = InMemorySaver()

# 이전 대화 내용 표시
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])


# LangGraph 워크플로우 인스턴스 생성
app = graph_workflow(checkpoint=st.session_state["checkpoint"])

# 사용자 입력 받기
if question := st.chat_input("메시지를 입력하세요..."):
    st.session_state["messages"].append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    # LangGraph 워크플로우에 질문 전달
    try:
        print(f"🧔‍사용자 질문) {question}\n")
        before_state = app.get_state(st.session_state["config"])
        print("💩대답전 User의 저장된 상태:", before_state.values)
        # print("💩대답전 config", st.session_state["config"])

        # print("💩이전 대화들..", st.session_state["messages"])
        response = app.invoke({"input": question, "messages": [("user", question)]}, config=st.session_state["config"])
        # 응답 메시지 추출 (마지막 메시지의 content)
        if "messages" in response and response["messages"]:
            if isinstance(response["messages"][-1], AIMessage):
                answer = response["messages"][-1].content
            else:
                answer = "아직 미완성된 Workflow의 답변입니다."
        else:
            answer = str(response)
    except Exception as e:
        answer = f"에러 발생으로 인해 이전 대화로 복구합니다."
        print(f"💥질문 '{question}'에 대한 에러 발생..\n{e}")
        print("========================================\n",traceback.format_exc(),"\n========================================")
        
        # last_stable_state = app.get_state(st.session_state["config"])
        # print(last_stable_state.values)
        # app.update_state(st.session_state["config"], last_stable_state.values)

        # checkpoints = list(app.get_state_history(st.session_state["config"]))
        # if len(checkpoints) > 1:
        #     previous_state = checkpoints[1].values
        #     print(previous_state)
        #     app.update_state(st.session_state["config"], previous_state)

        print(before_state.values, "로 복구..")
        app.update_state(st.session_state["config"], before_state.values.copy())
        check_state = app.get_state(st.session_state["config"])
        if before_state.values != check_state.values:
            print(check_state.values)


    saved_state = app.get_state(st.session_state["config"])
    print("💀User의 저장된 상태:", saved_state.values)
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer) 