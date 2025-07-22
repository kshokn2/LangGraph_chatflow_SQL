from pydantic import BaseModel, Field
from typing import Annotated, Literal, List


report_agent_list = ["Data Analysis", "Visualization", "Domain Knowledge"]

class Step(BaseModel):
    """Sorted steps to execute the plan with a agent"""
    agent: Literal[*report_agent_list]
    task_description: str

class Plan(BaseModel):
    """Sorted steps to execute the plan with a agent"""
    steps: Annotated[List[Step], "Different steps to follow, should be in sorted order"]
