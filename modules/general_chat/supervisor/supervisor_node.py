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
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", general_supervisor_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next? "
                "Or should we FINISH? Select one of: {options}",
            ),
        ]
    ).partial(options=str(route_options_for_next), tool_list=", ".join(general_tool_list))

    general_supervisor_chain = prompt | llm.with_structured_output(RouteResponse) 

    input_for_next = [HumanMessage(content=state["input"])] + state["messages"]
    print(f"✅ input_for_next.... {input_for_next}")

    result = general_supervisor_chain.invoke({"messages": 
        input_for_next
        }
    )

    print(f"✅ wrap_general_supervisor의 출력: {result}\n")

    return result

def get_next(state: PlanExecute):
    return state["next"]

