

from crud.auth import UserCRUD
from routers.auth_router import get_user
from fastapi.testclient import TestClient
from schemas.schemas import UserInDB
from sqlalchemy.orm import Session


PASSWORD_TESTE = 'random-passW0rd'


def user_authentication_headers(client: TestClient, username: str, password: str):
    """ Retorna token para o usuário """
    data = {"username": username, "password": PASSWORD_TESTE}
    r = client.post("/api/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    refresh_token = response["refresh_token"]
    headers = {"Authorization": f"Bearer {auth_token}", "refresh_token": refresh_token}
    return headers


def authentication_token(client: TestClient, username: str, db: Session):
    """
    Retorna um token valido se nao existir ele sera criado para os testes
    """
    user = get_user(username=username, db=db)
    if not user:
        user_in_create = UserInDB(username=username, password=PASSWORD_TESTE)
        user = UserCRUD(db).criar(user_in_create)
    return user_authentication_headers(client=client, username=username, password=PASSWORD_TESTE)