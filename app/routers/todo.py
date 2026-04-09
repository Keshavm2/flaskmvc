from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.database import SessionDep
from app.auth import AuthDep
from app.models.todo import Todo, TodoBase
from app.repositories.todo import TodoRepository
from app.utilities.flash import flash
from . import templates

todos_router = APIRouter(prefix="/todos", tags=["Todos"])

@todos_router.get("/", response_class=HTMLResponse)
async def todos_page(request: Request, user: AuthDep, db: SessionDep):
    repo = TodoRepository(db)
    todos = repo.get_by_user(user.id)
    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={"user": user, "todos": todos}
    )

@todos_router.post("/create")
async def create_todo(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    title: str = Form(...),
    description: str = Form(default=""),
):
    repo = TodoRepository(db)
    repo.create(TodoBase(title=title, description=description, user_id=user.id))
    flash(request, "Todo created!", "success")
    return RedirectResponse(url="/todos/", status_code=status.HTTP_303_SEE_OTHER)

@todos_router.post("/delete/{todo_id}")
async def delete_todo(
    todo_id: int,
    request: Request,
    user: AuthDep,
    db: SessionDep,
):
    repo = TodoRepository(db)
    todo = repo.get_by_id(todo_id)
    if not todo or todo.user_id != user.id:
        flash(request, "Todo not found.", "danger")
        return RedirectResponse(url="/todos/", status_code=status.HTTP_303_SEE_OTHER)
    repo.delete(todo_id)
    flash(request, "Todo deleted.", "success")
    return RedirectResponse(url="/todos/", status_code=status.HTTP_303_SEE_OTHER)

@todos_router.post("/toggle/{todo_id}")
async def toggle_todo(
    todo_id: int,
    request: Request,
    user: AuthDep,
    db: SessionDep,
):
    repo = TodoRepository(db)
    todo = repo.get_by_id(todo_id)
    if not todo or todo.user_id != user.id:
        flash(request, "Todo not found.", "danger")
        return RedirectResponse(url="/todos/", status_code=status.HTTP_303_SEE_OTHER)
    repo.update(todo_id, todo.title, todo.description, not todo.completed)
    return RedirectResponse(url="/todos/", status_code=status.HTTP_303_SEE_OTHER)