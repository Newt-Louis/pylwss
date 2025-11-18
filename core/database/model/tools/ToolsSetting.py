from typing import Optional
from pydantic import BaseModel, Field

class ToolsSetting(BaseModel):
    id: Optional[int] = None
    type: str
    port: int = Field(default=3306)
    root_path: str
    is_chosen: bool = Field(default=False)

    class Config:
        extra = "ignore"