from models.burgers import Burger

def test_burgers_erro_autenticacao(client):
    """ Teste ao acessar lista de burgers sem autenticacao """
    response = client.get("/api/burger")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    
def test_burgers_autenticado(client, burgers, header_access_token):
    """ Teste lista de burgers quando autenticado """
    response = client.get("/api/burger", headers=header_access_token)
    assert response.status_code == 200

    assert response.json() == [
        {
            'id': 3, 'nome': 'João', 'carne': 'Maminha', 'pao': 'Italiano',
            'preco': 29.99, 'status': 'Pendente',
            'opcionais': ['Barbecue', 'Mostarda']
        },
        {
            'id': 4, 'nome': 'Maria', 'carne': 'Maminha', 'pao': 'Italiano',
            'preco': 15.00, 'status': 'Pendente',
            'opcionais': []
        }
    ]


def test_burger_erro_autenticacao(client, burgers):
    """ Teste ao acessar 1 burger sem autenticacao """
    burger = burgers[-1]
    response = client.get(f"/api/users/{burger.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

    
def test_burger_autenticado(client, burgers, header_access_token):
    """ Teste exibindo 1 burger quando autenticado """
    burger = burgers[-1]
    response = client.get(f"/api/burger/{burger.id}", headers=header_access_token)
    assert response.status_code == 200

    assert response.json() == {
        'id': 4, 'nome': 'Maria', 'carne': {'id': 1, 'descricao': 'Maminha'},
        'pao': {'id': 2, 'descricao': 'Italiano'}, 'preco': 15.0,
        'opcionais': [], 'status': {'descricao': 'Pendente'}
    }
    
def test_post_burger(client, ingredientes, opcionais, status):
    """ Teste incluir burger """
    carne_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'C'][0]
    pao_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'P'][0]
    opcional1_burger, opcional2_burger = opcionais[-2:]
    status_burger = status[-1]
    dados =  {
        "nome": "Ricardo",
        "carne": carne_burger.id,
        "pao": pao_burger.id,
        "preco": 18.99,
        "opcionais": [
            opcional1_burger.id,
            opcional2_burger.id,

        ],
        "status": status_burger.id
    }
    response = client.post("/api/burger", json=dados)
    assert response.status_code == 201
    dados_burger = response.json()
    assert dados_burger["nome"] == dados["nome"] 
    assert dados_burger["carne"]["descricao"] == carne_burger.descricao
    assert dados_burger["pao"]["descricao"] == pao_burger.descricao 
    assert dados_burger["preco"] == dados["preco"] 
    assert dados_burger["status"]["descricao"] == status_burger.descricao 
    assert dados_burger["opcionais"] == [
        {'descricao': opcional.descricao } for opcional in (opcional1_burger, opcional2_burger)
    ]


def test_patch_burger_nao_autorizado(client, burgers, ingredientes, opcionais, status):
    """ Teste atualizar burger com patch """
    carne_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'C'][-1]
    pao_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'P'][-1]
    opcional1_burger, opcional2_burger = opcionais[:2]
    status_burger = status[0]
    ultimo_burger = burgers[-1]

    dados =  {
        "nome": "Novo nome",
        "carne_id": carne_burger.id,
        "pao_id": pao_burger.id,
        "preco": 9.99,
        "opcionais": [
            opcional1_burger.id,
            opcional2_burger.id,
        ],
        "status_id": status_burger.id
    }
    response = client.patch(f"/api/burger/{ultimo_burger.id}", json=dados)
    assert response.status_code == 401

def test_patch_burger_autorizado(client, burgers, ingredientes, opcionais, status, header_access_token):
    """ Teste atualizar burger com patch """
    carne_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'C'][-1]
    pao_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'P'][-1]
    opcional1_burger, opcional2_burger = opcionais[:2]
    status_burger = status[0]
    ultimo_burger = burgers[-1]

    dados =  {
        "nome": "Novo nome",
        "carne_id": carne_burger.id,
        "pao_id": pao_burger.id,
        "preco": 9.99,
        "opcionais": [
            opcional1_burger.id,
            opcional2_burger.id,
        ],
        "status_id": status_burger.id
    }
    response = client.patch(f"/api/burger/{ultimo_burger.id}", json=dados, headers=header_access_token)
    assert response.status_code == 200
    dados_burger = response.json()
    assert dados_burger["nome"] == dados["nome"] 
    assert dados_burger["carne"]["descricao"] == carne_burger.descricao
    assert dados_burger["pao"]["descricao"] == pao_burger.descricao 
    assert dados_burger["preco"] == dados["preco"] 
    assert dados_burger["status"]["descricao"] == status_burger.descricao 
    assert dados_burger["opcionais"] == [
        {'descricao': opcional.descricao } for opcional in (opcional1_burger, opcional2_burger)
    ]

def test_put_burger_nao_autorizado(client, burgers, ingredientes, opcionais, status):
    """ Teste atualizar burger com put nao autorizado"""
    carne_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'C'][-1]
    pao_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'P'][-1]
    opcional1_burger, opcional2_burger = opcionais[:2]
    status_burger = status[0]
    primeiro_burger = burgers[0]

    dados =  {
        "nome": "Nome atualizado",
        "carne": carne_burger.id,
        "pao": pao_burger.id,
        "preco": 5.99,
        "opcionais": [
            opcional1_burger.id,
            opcional2_burger.id,
        ],
        "status": status_burger.id
    }
    response = client.put(f"/api/burger/{primeiro_burger.id}", json=dados)
    assert response.status_code == 401

def test_put_burger_autorizado(client, burgers, ingredientes, opcionais, status, header_access_token):
    """ Teste atualizar burger com put """
    carne_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'C'][-1]
    pao_burger = [ingrediente for ingrediente in ingredientes if ingrediente.tipo == 'P'][-1]
    opcional1_burger, opcional2_burger = opcionais[:2]
    status_burger = status[0]
    primeiro_burger = burgers[0]

    dados =  {
        "nome": "Nome atualizado",
        "carne": carne_burger.id,
        "pao": pao_burger.id,
        "preco": 5.99,
        "opcionais": [
            opcional1_burger.id,
            opcional2_burger.id,
        ],
        "status": status_burger.id
    }
    response = client.put(f"/api/burger/{primeiro_burger.id}", json=dados, headers=header_access_token)
    assert response.status_code == 200
    dados_burger = response.json()
    assert dados_burger["nome"] == dados["nome"] 
    assert dados_burger["carne"]["descricao"] == carne_burger.descricao
    assert dados_burger["pao"]["descricao"] == pao_burger.descricao 
    assert dados_burger["preco"] == dados["preco"] 
    assert dados_burger["status"]["descricao"] == status_burger.descricao 
    assert dados_burger["opcionais"] == [
        {'descricao': opcional.descricao } for opcional in (opcional1_burger, opcional2_burger)
    ]

def test_delete_burger_nao_autorizado(client, db_session):
    """ Teste deletando burger nao autorizado"""
    total = db_session.query(Burger).count()
    burger = db_session.query(Burger).all()[0]
    response = client.delete(f"/api/burger/{burger.id}")
    assert response.status_code == 401
    total_new = db_session.query(Burger).count()
    assert total == total_new

def test_delete_burger_autorizado(client, db_session, header_access_token):
    """ Teste deletando burger """
    total = db_session.query(Burger).count()
    burger = db_session.query(Burger).all()[0]
    response = client.delete(f"/api/burger/{burger.id}", headers=header_access_token)
    assert response.status_code == 200
    total_new = db_session.query(Burger).count()
    assert total-1 == total_new

