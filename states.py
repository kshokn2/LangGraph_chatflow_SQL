import operator
from dataclasses import dataclass, field
from pydantic import BaseModel
from typing import Annotated, TypedDict, Literal, Optional, List, Dict, Tuple, Union
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.managed import IsLastStep


# 상태 정의
class PlanExecute(TypedDict):
    input: Annotated[str, "User's input"]
    route_chatbot: Annotated[str, "Selected chatbot"]
    plan: Annotated[List[str], "Current plan"]
    past_steps: Annotated[List[Tuple], operator.add]
    response: Annotated[str, "Final response"]
    messages: Annotated[List[BaseMessage], add_messages]
    agents: List[str]
    next: str
    is_last_step: Annotated[IsLastStep, "last step"] = field(default=False)
    """
    # PlanExecute에서 필드 정리
    - input: 사용자의 입력
    - plan: 현재 계획
    - past_steps: 이전에 실행한 계획과 실행 결과
    - response: 최종 응답
    - (추가된 필드) messages: 메세지
    - (추가된 필드) agents: 멤버 에이전트 목록
    - (추가된 필드) next: Supervisior 에이전트에게 다음 작업자를 선택하도록 지시
    """
