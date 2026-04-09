from sqlmodel import Session, select, func
from app.models.todo import TodoBase, Todo
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, todo_data: TodoBase) -> Todo:
        try:
            todo_db = Todo.model_validate(todo_data)
            self.db.add(todo_db)
            self.db.commit()
            self.db.refresh(todo_db)
            return todo_db
        except Exception as e:
            logger.error(f"An error occurred while saving todo: {e}")
            self.db.rollback()
            raise

    def get_by_user(self, user_id: int) -> list[Todo]:
        return self.db.exec(select(Todo).where(Todo.user_id == user_id)).all()

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        return self.db.get(Todo, todo_id)

    def update(self, todo_id: int, title: str, description: str, completed: bool) -> Todo:
        todo = self.db.get(Todo, todo_id)
        if not todo:
            raise Exception("Todo not found")
        todo.title = title
        todo.description = description
        todo.completed = completed
        try:
            self.db.add(todo)
            self.db.commit()
            self.db.refresh(todo)
            return todo
        except Exception as e:
            logger.error(f"An error occurred while updating todo: {e}")
            self.db.rollback()
            raise

    def delete(self, todo_id: int):
        todo = self.db.get(Todo, todo_id)
        if not todo:
            raise Exception("Todo not found")
        try:
            self.db.delete(todo)
            self.db.commit()
        except Exception as e:
            logger.error(f"An error occurred while deleting todo: {e}")
            self.db.rollback()
            raise