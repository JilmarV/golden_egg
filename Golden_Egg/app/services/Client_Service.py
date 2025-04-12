from sqlalchemy.orm import Session
from repositories.Client_Repository import create_Client, get_Client
from schemas.Client_Schema import ClientCreate


def create_new_client(db: Session, client: ClientCreate):
    return create_Client(db, client)


def fetch_client(db: Session, client_id: int):
    return get_Client(db, client_id)