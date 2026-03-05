from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_products_empty():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []

def test_create_product():
    product_data = {
        "nom": "Produit Test",
        "description": "Une description",
        "prix": 29.99,
        "quantite_stock": 10
    }
    response = client.post("/products", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nom"] == "Produit Test"
    assert "id" in data
    
    # On mémorise l'id pour les prochains tests
    return data["id"]

def test_read_product_success():
    # Dépendance implicite au test précédent pour simplicité ou on recrée un
    product_data = {"nom": "A", "prix": 1.0, "quantite_stock": 1}
    create_response = client.post("/products", json=product_data)
    p_id = create_response.json()["id"]

    response = client.get(f"/products/{p_id}")
    assert response.status_code == 200
    assert response.json()["nom"] == "A"

def test_read_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404

def test_update_product():
    product_data = {"nom": "B", "prix": 2.0, "quantite_stock": 2}
    create_response = client.post("/products", json=product_data)
    p_id = create_response.json()["id"]

    update_data = {"prix": 2.5}
    response = client.put(f"/products/{p_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["prix"] == 2.5
    assert response.json()["nom"] == "B" # Le nom reste le même

def test_update_product_not_found():
    response = client.put("/products/999", json={"prix": 2.5})
    assert response.status_code == 404

def test_delete_product():
    product_data = {"nom": "C", "prix": 3.0, "quantite_stock": 3}
    create_response = client.post("/products", json=product_data)
    p_id = create_response.json()["id"]

    response = client.delete(f"/products/{p_id}")
    assert response.status_code == 204

    # Vérification que c'est bien supprimé
    response_get = client.get(f"/products/{p_id}")
    assert response_get.status_code == 404

def test_delete_product_not_found():
    response = client.delete("/products/999")
    assert response.status_code == 404

def test_create_invalid_product():
    response = client.post("/products", json={"nom": "D"}) # Missing required fields
    assert response.status_code == 422
