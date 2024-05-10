from datetime import datetime

from sqlalchemy import create_engine
import databasemodels as dbm
from sqlalchemy.orm import Session


engine = create_engine('sqlite+pysqlite:///todo.db', echo=True)
dbm.Base.metadata.create_all(engine)

with Session(engine) as session:
    chloe = dbm.User(
        name="chloe",
        fullname="Chloe Cornelissen",
        addresses=[dbm.Address(email_adress="chloecornelissen@hotmail.com")],
        password_hash="default"
    )
    chloe.set_password("chloe123")

    admin = dbm.User(
        name="admin",
        fullname="admin",
        addresses=[dbm.Address(email_adress="admin@admin.admin")],
        password_hash="default"
    )
    admin.set_password("admin")
    session.add_all([chloe, admin])
    session.commit()

    new_todo = dbm.TodoList(
        todo_text="This is a new todo",
        todo_made_time=datetime.now(),
        todo_date=datetime(2024, 5, 10),
        todo_date_overdue=False,
        todo_done=False,
        user_id=chloe.id,
    )

    session.add(new_todo)
    session.commit()
