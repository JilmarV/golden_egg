from sqlalchemy.orm import Session
from models.Client import Client
from schemas.Client_Schema import ClientCreate


def create_Client(db: Session, client: ClientCreate):
    db_Client = Client(**client.dict())
    db.add(db_Client)
    db.commit()
    db.refresh(db_Client)
    return db_Client

def get_Client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()