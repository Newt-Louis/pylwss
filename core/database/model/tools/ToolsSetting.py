from typing import Optional
from pydantic import BaseModel, Field

class ToolsSetting(BaseModel):
    id: Optional[int] = None
    type: str
    port: int = Field(default=0000)
    root_path: Optional[str] = None
    is_chosen: bool = Field(default=False)

    class Config:
        extra = "ignore"