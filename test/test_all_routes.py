from fastapi.testclient import TestClient
from main import app
import random, string
from datetime import datetime

client = TestClient(app)

def unique_email():
    return f"test.user_{int(datetime.now().timestamp())}@example.com"

def unique_product_name():
    return "TestProduct_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def test_all_routes():
    # USER TESTS
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": unique_email(),
        "phone_number": "123456789",
        "address": "123 Test St",
        "zip_code": 12345,
        "city": "Testville",
        "is_admin": False,
        "company": "TestCorp"
    }

    print("\n-- CREATE USER --")
    response = client.post("/api/users/", json=user_data)
    print(response.status_code, response.json())
    assert response.status_code == 200

    response = client.get("/api/users/")
    created_user = response.json()[-1]
    user_id = created_user["id"]

    print("\n-- GET USER BY ID --")
    print(client.get(f"/api/users/{user_id}").json())

    print("\n-- UPDATE USER --")
    print(client.put(f"/api/users/{user_id}", json={"city": "UpdatedTown"}).json())

    print("\n-- DELETE USER --")
    print(client.delete(f"/api/users/{user_id}").json())

    # PRODUCT TESTS
    product_data = {
        "name": unique_product_name(),
        "unit": "piece",
        "price": 9.99,
        "description": "A test product",
        "stock": 10
    }

    print("\n-- CREATE PRODUCT --")
    response = client.post("/api/products/", json=product_data)
    print(response.status_code, response.json())
    assert response.status_code == 200

    response = client.get("/api/products/")
    created_product = response.json()[-1]
    product_id = created_product["id"]

    print("\n-- GET PRODUCT BY ID --")
    print(client.get(f"/api/products/{product_id}").json())

    print("\n-- UPDATE PRODUCT --")
    print(client.put(f"/api/products/{product_id}", json={"price": 19.99}).json())

    print("\n-- DELETE PRODUCT --")
    print(client.delete(f"/api/products/{product_id}").json())

if __name__ == "__main__":
    test_all_routes()
