from pydantic import BaseModel
from typing import List, Optional

class ToolConfig(BaseModel):
    function_name: str
    ai_description: str
    tool_name: Optional[str] = None
    regenerate: bool = False


class ToolGroup(BaseModel):
    name: str
    tools: List[ToolConfig]
