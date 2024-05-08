from sqlalchemy import create_engine
import databasemodels as dbm
from sqlalchemy.orm import Session


engine = create_engine('sqlite://', echo=True)
dbm.Base.metadata.create_all(engine)

with Session(engine) as session:
    chloe = dbm.User(
        name="Chloe",
        fullname="Chloe Cornelissen",
        addresses=[dbm.Address(email_adress="chloecornelissen@hotmail.com")],
    )
    admin = dbm.User(
        name="admin",
        fullname="admin",
        addresses=[dbm.Address(email_adress="admin@admin.admin")]
    )
    session.add_all([chloe, admin])
    session.commit()