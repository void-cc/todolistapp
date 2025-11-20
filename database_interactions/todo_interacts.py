from databasemodels import TodoList
from sqlalchemy import select
from createengine import sessiondatabase as sdb
from datetime import datetime


def get_todo_by_id(todo_id):
    stmt = select(TodoList).where(TodoList.id == todo_id)
    return sdb.execute(stmt).scalar_one_or_none()

def get_todo_function(user_id):
    todolist = []
    stmt = select(TodoList).where(TodoList.user_id == user_id)
    result = sdb.execute(stmt)
    for user_obj in result.scalars():
        todolist.append(
            {'todo_text': user_obj.todo_text,
             'todo_made_time': user_obj.todo_made_time,
             'todo_date': user_obj.todo_date.isoformat() if user_obj.todo_date else None,
             'todo_date_overdue': user_obj.todo_date_overdue,
             'todo_done': user_obj.todo_done,
             'user_id': user_obj.user_id,
             'id': user_obj.id,
             'tags': user_obj.tags
             }
        )
    return todolist


def add_to_todo(todo_text,
                user_id,
                todo_date=None,
                tags=None,
                todo_date_overdue=False,
                todo_done=False,
                ):
    if todo_date:
        todo_date = datetime.fromisoformat(todo_date)
    new_todo = TodoList(
        todo_text=todo_text,
        todo_made_time=datetime.now(),
        todo_date=todo_date,
        tags=tags,
        todo_date_overdue=todo_date_overdue,
        todo_done=todo_done,
        user_id=user_id
    )
    sdb.add(new_todo)
    sdb.commit()


def change_todo_done(todo_id, todo_done):
    stmt = select(TodoList).where(TodoList.id == todo_id)
    result = sdb.execute(stmt)
    for user_obj in result.scalars():
        user_obj.todo_done = todo_done
    sdb.commit()


def change_todo_date(todo_id, todo_date):
    if todo_date:
        todo_date = datetime.fromisoformat(todo_date)
    stmt = select(TodoList).where(TodoList.id == todo_id)
    result = sdb.execute(stmt)
    for user_obj in result.scalars():
        user_obj.todo_date = todo_date
    sdb.commit()


def change_todo_text(todo_id, todo_text):
    stmt = select(TodoList).where(TodoList.id == todo_id)
    result = sdb.execute(stmt)
    for user_obj in result.scalars():
        user_obj.todo_text = todo_text
    sdb.commit()


def change_todo_tags(todo_id, tags):
    stmt = select(TodoList).where(TodoList.id == todo_id)
    result = sdb.execute(stmt)
    for user_obj in result.scalars():
        user_obj.tags = tags
    sdb.commit()


def delete_todo(todo_id):
    stmt = select(TodoList).where(TodoList.id == todo_id)
    result = sdb.execute(stmt)
    for user_obj in result.scalars():
        sdb.delete(user_obj)
    sdb.commit()
