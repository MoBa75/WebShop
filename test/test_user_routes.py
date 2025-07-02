import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_user_routes():
    # E-Mail ist eindeutig durch Zeitstempel
    email = f"test.user_{int(time.time())}@example.com"

    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": email,
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

    # GET ALL USERS to retrieve ID
    print("\n-- GET ALL USERS --")
    response = client.get("/api/users/")
    print(response.status_code, response.json())
    users = response.json()
    assert isinstance(users, list)
    user_id = users[-1]["id"]  # Nimm den zuletzt erstellten

    print("\n-- GET USER BY ID --")
    response = client.get(f"/api/users/{user_id}")
    print(response.status_code, response.json())

    print("\n-- UPDATE USER --")
    response = client.put(f"/api/users/{user_id}", json={
        "city": "UpdatedCity",
        "first_name": "UpdatedName"
    })
    print(response.status_code, response.json())

    print("\n-- UPDATE NON-EXISTENT USER --")
    response = client.put("/api/users/99999", json={
        "city": "Nowhere"
    })
    print(response.status_code, response.json())

    print("\n-- DELETE USER --")
    response = client.delete(f"/api/users/{user_id}")
    print(response.status_code, response.json())

    print("\n-- DELETE NON-EXISTENT USER --")
    response = client.delete("/api/users/99999")
    print(response.status_code, response.json())

if __name__ == "__main__":
    test_user_routes()
