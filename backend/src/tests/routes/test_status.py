from models.burgers import Status

    
def test_get_status(client, status):
    """ Teste exibindo todos os status """
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "descricao": "Pendente" },
        {"id": 2, "descricao": "Produção"},
        {"id": 3, "descricao": "Finalizado"}
    ]

def test_post_status(client):
    """ Teste incluir status """
    dados = {"descricao": "Preparo"}
    response = client.post("/api/status", json=dados)
    assert response.status_code == 201

    dados_status = response.json()
    assert dados["descricao"] == dados_status["descricao"] 


def test_delete_status(client, db_session):
    """ Teste deletando status """
    total = db_session.query(Status).count()
    status = db_session.query(Status).all()[0]
    response = client.delete(f"/api/status/{status.id}")
    assert response.status_code == 200
    total_new = db_session.query(Status).count()
    assert total-1 == total_new


