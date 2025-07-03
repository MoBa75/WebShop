from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_user_error_cases():
    print("\n-- CREATE DUPLICATE USER --")
    user_data = {
        "first_name": "Error",
        "last_name": "User",
        "email": "duplicate@example.com",
        "phone_number": "123456789",
        "address": "123 Duplicate St",
        "zip_code": 12345,
        "city": "Errorville",
        "is_admin": False,
        "company": "ErrorCorp"
    }

    # Erster Versuch: sollte funktionieren
    client.post("/api/users/", json=user_data)

    # Zweiter Versuch: sollte Fehler liefern
    response = client.post("/api/users/", json=user_data)
    print(response.status_code, response.json())
    assert response.status_code == 409
    assert response.json()["detail"] == "A user with this email already exists."

    print("\n-- CREATE USER WITH INVALID EMAIL --")
    invalid_user = user_data.copy()
    invalid_user["email"] = "invalid-email"
    response = client.post("/api/users/", json=invalid_user)
    print(response.status_code, response.json())
    assert response.status_code == 422

    print("\n-- CREATE USER WITH FUTURE BIRTH DATE --")
    future_birth_user = user_data.copy()
    future_birth_user["email"] = "future@example.com"
    future_birth_user["birth_date"] = "3000-01-01"
    response = client.post("/api/users/", json=future_birth_user)
    print(response.status_code, response.json())
    assert response.status_code == 422
    assert "Birth date cannot be in the future" in str(response.json())

    print("\n-- CREATE USER WITH BIRTH DATE TOO FAR IN PAST --")
    old_birth_user = user_data.copy()
    old_birth_user["email"] = "old@example.com"
    old_birth_user["birth_date"] = "1900-01-01"
    response = client.post("/api/users/", json=old_birth_user)
    print(response.status_code, response.json())
    assert response.status_code == 422
    assert "Birth date is too far in the past" in str(response.json())

    print("\n-- UPDATE NON-EXISTENT USER --")
    response = client.put("/api/users/9999", json={"city": "Nowhere"})
    print(response.status_code, response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."


def test_product_error_cases():
    print("\n-- CREATE DUPLICATE PRODUCT --")
    product_data = {
        "name": "FehlerTestProdukt",
        "unit": "kg",
        "price": 12.99,
        "description": "Testprodukt",
        "stock": 20
    }

    client.post("/api/products/", json=product_data)

    response = client.post("/api/products/", json=product_data)
    print(response.status_code, response.json())
    assert response.status_code == 409
    assert response.json()["detail"] == "A product with this name already exists."

    print("\n-- CREATE PRODUCT WITH NEGATIVE PRICE --")
    negative_price = product_data.copy()
    negative_price["name"] = "NegativerPreis"
    negative_price["price"] = -5.0
    response = client.post("/api/products/", json=negative_price)
    print(response.status_code, response.json())
    assert response.status_code == 422
    assert any("greater than or equal to 0" in err["msg"] for err in response.json()["detail"])

    print("\n-- CREATE PRODUCT WITH NEGATIVE STOCK --")
    negative_stock = product_data.copy()
    negative_stock["name"] = "NegativerLager"
    negative_stock["stock"] = -10
    response = client.post("/api/products/", json=negative_stock)
    print(response.status_code, response.json())
    assert response.status_code == 422
    assert any("greater than or equal to 0" in err["msg"] for err in response.json()["detail"])

    print("\n-- UPDATE NON-EXISTENT PRODUCT --")
    response = client.put("/api/products/9999", json={"stock": 100})
    print(response.status_code, response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found."
