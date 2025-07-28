from pydantic import BaseModel
from typing import Literal, List
from langchain_core.messages import HumanMessage, RemoveMessage, BaseMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from models import * # llm
from states import PlanExecute # state

from .schema import RouteResponse, general_tool_list, route_options_for_next
from .prompt import *


def wrap_general_supervisor(state: PlanExecute):
    import config
    
    print(f"✅ wrap_general_supervisor의 Input(state) 확인: {state}")
    last_message = state["messages"][-1]
    if isinstance(last_message, AIMessage): type_last_message = "AIMessage"
    elif isinstance(last_message, HumanMessage): type_last_message = "HumanMessage"
    else: type_last_message = "Not Important"
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", general_supervisor_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next? Or should we FINISH?\n\n"
                "In this setting, the user typically asks a question. And one of the agents responds to that question or Nothing responds yet.\n"
                "You are responsible for reviewing the conversation so far, including the most recent response, and deciding the next step.\n"
                "Make your decision strictly based on the responsibilities described above.\n"
                "Do not assume anything beyond the given messages.\n"
                "If 'type_last_msg' is 'HumanMessage' type, **DO NOT SELECT the 'FINISH'**\n\n"
                "type_last_msg: {type_last_msg}\n"
                "Select one of: {options} as 'next' of output"
                ", and tell me why does you select that 'next' action in 'reason' field of output.\n"
                "Find the most recent user's question in the conversation above and fill in the 'question' field of output.\n"
                "Also find agent's response to 'question' field of output in the conversation above, and fill in the 'agent_response' field of output. If there is no response to 'question' field yet, fill in 'agent_response' field with the string 'None'."
                
                # "Given the conversation above, determine who should act next or if the conversation should FINISH and why should be.\n"
                # "If the previous agent's response indicates missing context, an inability to proceed, or a request for clarification,"
                # "then respond with FINISH.\n"
                # "Select one of: {options}\n"
                
                # "Examples of 'FINISH' responses include:\n"
                # "- 죄송합니다. 답변을 하기위한 필요한 정보가 주어지지 않았습니다.\n"
                # "- 정확한 답변을 하려면 추가적인 정보가 필요합니다.\n"
                # "- 입력된 데이터가 부족하여 분석을 수행할 수 없습니다."
            ),
        ]
    ).partial(type_last_msg=type_last_message, options=str(route_options_for_next), tool_list=", ".join(general_tool_list))

    general_supervisor_chain = prompt | llm.with_structured_output(RouteResponse) 

    # state["messages"] 관리 1
    if isinstance(last_message, AIMessage):
        if last_message.content == '' or last_message.response_metadata["finish_reason"] == "MALFORMED_FUNCTION_CALL":
            print(f"❌ 올바르지 않은 AIMessage ---> {state['messages'][-1]} <--- 삭제.")
            del state["messages"][-1]

    input_for_next = state["messages"]
        
    print(f"✅ input_for_next.... {input_for_next}")

    result = general_supervisor_chain.invoke(
        {"messages": input_for_next}
    )

    print(f"✅ wrap_general_supervisor의 출력: {result}\n")

    # state["messages"] 관리 2
    if result.next != "FINISH" and isinstance(last_message, AIMessage):
        print(f"❌ 새로운 Agent 호출하기 전에 이전 Agent의 AIMessage ---> '{last_message.content}' <--- 삭제.")
        del state["messages"][-1]

    return {"next": result.next}

def get_next(state: PlanExecute):
    return state["next"]

