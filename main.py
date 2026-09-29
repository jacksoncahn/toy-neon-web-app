from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from lib.auth import require_auth
from lib.cors import allowed_origins
from lib import database
from lib.models import (
    AddTodoRequest,
    EditTodoRequest,
    ErrorResponse,
    RemoveTodoRequest,
    SuccessResponse,
)

app = FastAPI(title="Toy Web App Neon", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins(),
    allow_methods=["*"],
    allow_headers=["*"],
    allow_private_network=True,
)


def error_response(status_code: int, detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(error=detail).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    return error_response(exc.status_code, detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    return error_response(400, str(exc.errors()))


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception):
    return error_response(500, str(exc))


@app.get("/api")
def health():
    return {"message": "ok"}


@app.post("/api/add", response_model=SuccessResponse)
def add_todo(body: AddTodoRequest, user_id: str = Depends(require_auth)):
    task_id = database.add_task(user_id, body.task, body.due)
    return SuccessResponse(user_id=user_id, task_id=str(task_id))


@app.post("/api/fetch", response_model=SuccessResponse)
def fetch_todos(user_id: str = Depends(require_auth)):
    todos = database.fetch_todos(user_id)
    return SuccessResponse(user_id=user_id, todos=todos)


@app.post("/api/edit", response_model=SuccessResponse)
def edit_todo(body: EditTodoRequest, user_id: str = Depends(require_auth)):
    updated_id = database.edit_task(
        user_id, body.task_id, body.task, body.due, body.complete
    )
    if updated_id is None:
        raise HTTPException(status_code=404, detail="Todo not found for this user")
    return SuccessResponse(user_id=user_id, task_id=str(updated_id))


@app.post("/api/remove", response_model=SuccessResponse)
def remove_todo(body: RemoveTodoRequest, user_id: str = Depends(require_auth)):
    removed_id = database.remove_task(user_id, body.task_id)
    if removed_id is None:
        raise HTTPException(status_code=404, detail="Todo not found for this user")
    return SuccessResponse(user_id=user_id, task_id=str(removed_id))
