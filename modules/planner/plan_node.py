from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from models import *
from states import PlanExecute

from .schema import Plan
from .prompt import planner_prompt2



def planner_node(state: PlanExecute):

    planner_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", planner_prompt2,),
            ("placeholder", "{messages}"),
        ]
    )

    planner = planner_prompt | llm.with_structured_output(Plan)

    plan = planner.invoke({
        "messages": [HumanMessage(content=state["input"]),]
    })

    for s in plan.steps:
        print(s)
    return {"plan": plan.steps}