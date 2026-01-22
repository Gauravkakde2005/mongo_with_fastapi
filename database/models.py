from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Todo(BaseModel):
    title: str
    description: str
    completed: bool = False
    is_deleted: bool = False
    created_at: Optional[float] = None
    update_at: Optional[float] = None
