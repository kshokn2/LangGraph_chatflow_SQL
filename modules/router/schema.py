from pydantic import BaseModel, Field
from typing import Annotated, Literal

# Chatbot Router's Schema
'''
class Route(BaseModel):
    # 최종
    step: Literal["report", "tableau", "general"] = Field(
        None, description="The next step in the routing process"
    )
    # 테스트
    step: Literal["report", "general"] = Field(
        None, description="The next step in the routing process"
    )
'''

class Route(BaseModel):
    # 최종
    # step: Annotated[Literal["report", "tableau", "general"], "The next step in the routing process"]
    
    # 테스트
    step: Annotated[Literal["report", "general"], "The next step in the routing process"]

