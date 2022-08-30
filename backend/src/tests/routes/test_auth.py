from jose import JWTError, jwt
from routers.auth_router import ACCESS_SECRET_KEY, REFRESH_SECRET_KEY,ALGORITHM

from models.auth import User
from tests.utils.user import PASSWORD_TESTE
from tests.conftest import USERNAME_TESTE


def test_get_users(client, users):
    """ Teste exibindo todos os usuarios """
    response = client.get("/api/users")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_users(client, users, header_access_token):
    """ Teste exibindo todos os usuarios """
    response = client.get("/api/users", headers=header_access_token)
    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'username': 'usuario1', 'full_name': 'usuario1 sobrenome', 'disabled': False},
        {'id': 2, 'username': 'usuario2', 'full_name': 'usuario2 sobrenome', 'disabled': True}, 
        {'id': 3, 'username': 'teste', 'full_name': None, 'disabled': False}
    ]

def test_get_user_nao_autenticado(client, db_session, users):
    """ Teste exibindo 1 usuário """
    user = db_session.query(User).filter_by(username = 'usuario1').one_or_none()
    response = client.get(f"/api/users/{user.username}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_user(client, db_session, header_access_token, users):
    """ Teste exibindo 1 usuário """
    user = db_session.query(User).filter_by(username = 'usuario1').one_or_none()
    response = client.get(f"/api/users/{user.username}", headers=header_access_token)
    assert response.status_code == 200
    dados_user = response.json()
    assert dados_user['username'] == "usuario1"
    assert dados_user['full_name'] == "usuario1 sobrenome"
    assert dados_user['disabled'] == False

def test_post_usuario(client):
    """ Teste incluir usuario """
    dados =  {
        'username': 'usuario_novo', 'password': 'minha_senha',
        'full_name': 'usuario1 sobrenome', 'disabled': False
    }
    response = client.post("/api/users", json=dados)
    assert response.status_code == 201
    dados_user = response.json()
    assert dados_user["username"] == dados["username"] 
    assert dados_user["full_name"] == dados["full_name"] 
    assert dados_user["disabled"] == dados["disabled"] 

def test_delete_usuario_nao_autenticado(client, db_session):
    """ Teste deletando usuario """
    total = db_session.query(User).count()
    user = db_session.query(User).all()[0]
    response = client.delete(f"/api/users/{user.username}")
    assert response.status_code == 401
    total_new = db_session.query(User).count()
    assert total == total_new

def test_delete_usuario(client, db_session, header_access_token):
    """ Teste deletando usuario """
    total = db_session.query(User).count()
    user = db_session.query(User).all()[0]
    response = client.delete(f"/api/users/{user.username}", headers=header_access_token)
    assert response.status_code == 200
    total_new = db_session.query(User).count()
    assert total-1 == total_new


def test_post_alterar_senha_nao_autenticado(client):
    """ Teste alterar senha sem estar autenticado"""
    dados =  {
        'old_password': PASSWORD_TESTE,
        'new_password': 'senha_nova'
    }
    response = client.put(
        "/api/users/change_my_password",
        json=dados
    )
    assert response.status_code == 401
    response.json() == {"detail": "Not authenticated"}

def test_post_alterar_senha(client, header_access_token):
    """ Teste alterar senha """
    dados =  {
        'old_password': PASSWORD_TESTE,
        'new_password': 'senha_nova'
    }
    response = client.put(
        "/api/users/change_my_password",
        json=dados,
        headers=header_access_token
    )
    assert response.status_code == 200
    response.json() == {"msg": "Senha alterada com sucesso"}

def test_post_tokens_dados_invalidos(client):
    """ Teste criar token com dados invalidos"""
    data = {"username": "usuario_inexiste", "password": "senha_errada"}
    response = client.post("/api/token", data=data)
    assert response.status_code == 401
    response.json() == {"detail": "Incorrect username or password"}

def test_post_tokens(client):
    """ Teste criar tokens """
    data = {"username": USERNAME_TESTE, "password": "senha_nova"}
    response = client.post("/api/token", data=data)
    assert response.status_code == 200
    dados_json = response.json()
    assert dados_json['token_type'] == "bearer"
    assert dados_json['username'] == USERNAME_TESTE
    
    # checa se access_token e valido
    access_token = dados_json["access_token"]
    payload = jwt.decode(access_token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    assert username is not None

    # checa se refresh_token e valido
    refresh_token = dados_json["refresh_token"]
    payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    assert username is not None

def test_post_refresh_token_invalido(client, header_access_token):
    """ Teste criar token usando refresh_token invalido """
    refresh_token = "zdWIiOiJ0ZXN0ZSIsImV4cCI6MTY2MjA2Mjk1MX0.bYeoXyYJ3NIlc2HeV-GGy2zFZaCBL7m3fCmnD6FW_XI"
    data = {"refresh_token": refresh_token}
    response = client.post("/api/token/refresh", json=data)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}

def test_post_refresh_token(client, header_access_token):
    """ Teste criar token usando refresh_token """
    refresh_token = header_access_token["refresh_token"]
    data = {"refresh_token": refresh_token}
    response = client.post("/api/token/refresh", json=data)
    assert response.status_code == 201
    dados_json = response.json()
 
    # checa se access_token e valido
    access_token = dados_json["access_token"]
    payload = jwt.decode(access_token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    assert username is not None
