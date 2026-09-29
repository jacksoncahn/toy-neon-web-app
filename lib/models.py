from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AddTodoRequest(BaseModel):
    task: str = Field(..., min_length=1)
    due: datetime


class EditTodoRequest(BaseModel):
    task_id: UUID
    task: str = Field(..., min_length=1)
    due: datetime
    complete: bool


class RemoveTodoRequest(BaseModel):
    task_id: UUID


class SuccessResponse(BaseModel):
    message: str = "Success"
    user_id: str
    task_id: str | None = None
    todos: list[dict] | None = None


class ErrorResponse(BaseModel):
    message: str = "Error"
    error: str
