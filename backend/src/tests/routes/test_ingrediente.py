from models.burgers import Ingrediente

    
def test_get_ingredientes(client, ingredientes):
    """ Teste exibindo todos os ingredientes """
    response = client.get("/api/ingrediente")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "descricao": "Maminha" },
        {"id": 2, "descricao": "Italiano"},
        {"id": 3, "descricao": "Patinho"},
        {"id": 4, "descricao": "3 Queijos"}
    ]

def test_post_ingrediente(client):
    """ Teste incluir ingrediente """
    dados = {
        "descricao": "Pão",
        "tipo": "P"
    }
    response = client.post("/api/ingrediente", json=dados)
    assert response.status_code == 201

    dados_ingrediente = response.json()
    assert dados["descricao"] == dados_ingrediente["descricao"] 
    assert dados["tipo"] == dados_ingrediente["tipo"]


def test_delete_ingrediente(client, db_session):
    """ Teste deletando ingrediente """
    total = db_session.query(Ingrediente).count()
    ingrediente = db_session.query(Ingrediente).all()[0]
    response = client.delete(f"/api/ingrediente/{ingrediente.id}")
    assert response.status_code == 200
    total_new = db_session.query(Ingrediente).count()
    assert total-1 == total_new


