from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, RemoveMessage, BaseMessage, SystemMessage, AIMessage, ToolMessage

from models import * # llm
from states import PlanExecute # state
from .tools.travel_tool import *
from .tools.math_tool import *
from .prompt import *


travel_agent = create_react_agent(
    model=llm,
    tools=[get_city_activities],
    prompt=travel_agent_prompt,
    name="travel_agent",
)

math_agent = create_react_agent(
    model=llm,
    tools=[add, multiply, divide],
    prompt=math_agent_prompt,
    name="math_agent",
)

def wrap_travel_agent(state: PlanExecute):
    import config
    # from langchain_core.runnables import RunnableConfig
    # from typing import Annotated, Any

    print("wrap_travel_agent의 input(state):", state)

    # supervisor_dict: dict[str, Any] = config.sub_configs.get("supervisor",{})
    # supervisor_config = RunnableConfig(**supervisor_dict)

    result = travel_agent.invoke({
        "messages": [
            HumanMessage(content=state["input"]),
        ]},
        # config=supervisor_config
    )
    print("wrap_travel_agent 출력:", result)
    # print(result['messages'][-1].content)
    print("============== tool 종료 ==============\n")
    return {"messages": [result['messages'][-1]]}


def wrap_math_agent(state: PlanExecute):
    import config
    # from langchain_core.runnables import RunnableConfig
    # from typing import Annotated, Any

    # print("wrap_math_agent", state)

    # supervisor_dict: dict[str, Any] = config.sub_configs.get("supervisor",{})
    # supervisor_config = RunnableConfig(**supervisor_dict)

    result = math_agent.invoke({
        "messages": [
            HumanMessage(content=state["input"]),
        ]},
        # config=supervisor_config
    )
    print("wrap_travel_agent 출력:", result)
    # print(result['messages'][-1].content)
    print("============== tool 종료 ==============\n")
    return {"messages": [result['messages'][-1]]}





# Agent Debug
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python node.py <call_agent> <question>")
        sys.exit(1)
    else:
        call_agent = sys.argv[1]
        question = sys.argv[2]

        print(f"{call_agent} Agent로 질문: {question}")

        if call_agent == "travel":
            result = travel_agent.invoke({
                "messages": [HumanMessage(content=question)]
            })
        elif call_agent == "math":
            result = math_agent.invoke({
                "messages": [HumanMessage(content=question)]
            })
        else:
            raise ValueError(f"잘못된 에이전트 선택({call_agent}). ['travel', 'math'] 중에 선택 필요..")
        
        print("travel_agent 출력:", result)