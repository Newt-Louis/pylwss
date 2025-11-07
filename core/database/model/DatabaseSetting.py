from typing import Optional
from pydantic import BaseModel, Field

class DatabaseSetting(BaseModel):
    id: Optional[int] = None
    type: str
    port: int = Field(default=3306)
    root_path: str
    executable_path: Optional[str] = None
    base_data_path: str
    ssl_cert_path: Optional[str] = None
    require_secure_transport: bool = Field(default=False)
    is_chosen: bool = Field(default=False)

    class Config:
        extra = "ignore"