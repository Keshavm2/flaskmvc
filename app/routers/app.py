from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import select
from app.database import SessionDep
from app.models import *
from app.auth import *
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import status
from . import templates

app_router = APIRouter()

@app_router.get("/app", response_class=HTMLResponse)
async def app(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    return templates.TemplateResponse(
        request=request, 
        name="app.html",
        context={
            "user": user
        }
    )

@app_router.get("/todos", response_class=HTMLResponse)
async def read_todos(
    request: Request,
    user: AuthDep,
    db: SessionDep,
    page: int = 1
):
    repo = TodoRepository(db)
    todos, pagination = repo.get_todos(page=page)
    
    return templates.TemplateResponse(
        request=request,
        name="todos.html",
        context={
            "user": user,
            "todos": todos,
            "pagination": pagination
        }
    )