from sqlmodel import Field, SQLModel
from typing import Optional

class TodoBase(SQLModel):
    title: str = Field(index=True)
    description: str = ""
    completed: bool = False
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)