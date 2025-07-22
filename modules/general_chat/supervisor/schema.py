from pydantic import BaseModel
from typing import Literal


general_tool_list = ["travel_agent", "math_agent"]
route_options_for_next = ["FINISH"] + general_tool_list

class RouteResponse(BaseModel):
    next: Literal[*route_options_for_next]