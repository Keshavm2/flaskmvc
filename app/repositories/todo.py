from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.todo import Todo
from app.utilities.pagination import Pagination

class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_todos(self, page: int = 1, limit: int = 10):
        offset = (page - 1) * limit

        db_qry = select(Todo)
        count_qry = select(func.count()).select_from(db_qry.subquery())
        total_count = self.db.execute(count_qry).scalar()

        todos = self.db.execute(db_qry.offset(offset).limit(limit)).scalars().all()
        pagination = Pagination(total_count=total_count, current_page=page, limit=limit)

        return todos, pagination