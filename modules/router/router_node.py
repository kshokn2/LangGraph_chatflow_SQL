# import modules.prompts as prompts
from models import *
from states import PlanExecute
# from modules.router.schema import Route
from .schema import Route
from .prompt import router_prompt

from langchain_core.messages import HumanMessage, SystemMessage


def chatbot_call_router(state: PlanExecute):
    """Route the input to the appropriate node"""
    # print("chatbot_call_router의 Input(state) 확인", state)

    router = llm.with_structured_output(Route)

    # Run the augmented LLM with structured output to serve as routing logic
    decision = router.invoke(
        [
            SystemMessage(content=router_prompt),
            HumanMessage(content=state["input"]),
        ]
    )

    return {"route_chatbot": decision.step}

def route_decision(state: PlanExecute):
    print(f"Log.. {state['route_chatbot']}으로 라우팅.")

    # Return the node name you want to visit next
    if state["route_chatbot"] == "report":
        return "route_report"
    # elif state["route_chatbot"] == "tableau":
    #     return "route_tableau"
    elif state["route_chatbot"] == "general":
        return "route_general"
    else:
        raise f'라우팅_에러: {state["route_chatbot"]}로 라우팅.. 예외 발생'