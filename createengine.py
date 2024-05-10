from sqlalchemy import create_engine
import databasemodels as dbm
from sqlalchemy.orm import Session


engine = create_engine('sqlite+pysqlite:///todo.db', echo=True)
dbm.Base.metadata.create_all(engine)


sessiondatabase = Session(engine)