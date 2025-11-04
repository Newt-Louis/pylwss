import os
from typing import Optional

from pydantic import BaseModel, field_validator, Field

class DatabaseSetting(BaseModel):
    id: Optional[int] = None
    type: str
    selected_version: str
    root_path: str
    executable_path: str
    base_data_path: str
    ssl_cert_path: Optional[str] = None
    require_secure_transport: bool = Field(default=False)

    class Config:
        extra = "ignore"