from langgraph.graph import StateGraph, START, END, MessagesState
# from langgraph.prebuilt import ToolNode, tools_condition
# from langchain_core.tools import tool
# from langchain_experimental.tools import PythonREPLTool, PythonAstREPLTool
# from langchain_experimental.utilities import PythonREPL
# from langchain_core.tracers import ConsoleCallbackHandler

from states import PlanExecute # state
from modules.router.router_node import chatbot_call_router, route_decision # router
from modules.planner.plan_node import planner_node
from modules.general_chat.supervisor.supervisor_node import wrap_general_supervisor, get_next # supervisor
from modules.general_chat.node import wrap_math_agent, wrap_travel_agent

def graph_workflow():
    workflow = StateGraph(PlanExecute)

    workflow.add_node("chatbot_call_router", chatbot_call_router)
    # workflow.add_node("report_supervisor", report_supervisor)

    # Data Analysis, Visualization, Domain Knowledge Agent 예시
    workflow.add_node("wrap_general_supervisor", wrap_general_supervisor)
    workflow.add_node("travel_agent", wrap_travel_agent)
    workflow.add_node("math_agent", wrap_math_agent)

    workflow.add_node("report_planner", planner_node)

    # 실행 흐름
    workflow.set_entry_point("chatbot_call_router")

    # supervisor 붙이기
    ## test 2
    workflow.add_conditional_edges(
        "chatbot_call_router",
        route_decision,
        {
            "route_report": "report_planner",
            "route_general": "wrap_general_supervisor",
            # "route_general": END,
    })

    workflow.add_conditional_edges("wrap_general_supervisor", get_next, {
        "travel_agent": "travel_agent",
        "math_agent": "math_agent",
        "FINISH": END,
    })
    workflow.add_edge("travel_agent", "wrap_general_supervisor")
    workflow.add_edge("math_agent", "wrap_general_supervisor")

    # workflow.add_edge("general_supervisor", END)
    # workflow.add_edge("report_supervisor", END)

    # 리포트 수행1
    # workflow.add_edge("report_planner", "report_agent_with_react") # react agent로 실행

    # 리포트 수행2
    # workflow.add_edge("report_planner", "report_agent_executor") # Send API로 실행

    # workflow.add_conditional_edges("Validator", lambda s: s["replan_needed"], {
    #     False: "FinalAnswer",
    #     True: "Planner"  # 재계획
    # })

    app = workflow.compile()

    return app