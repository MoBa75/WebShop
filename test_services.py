from datamanager.postgres_data_manager import PostgresDataManager
from datamanager.product_service import ProductService
from datamanager.user_service import UserService

# Initialisiere Datenmanager und Services
data_manager = PostgresDataManager()
product_service = ProductService(data_manager)
user_service = UserService(data_manager)

# Ergebnisliste
results = []

# ----------- 🧪 PRODUKT-TESTS ------------

# Produkt doppelt anlegen (sollte Fehler 409 erzeugen)
results.append(("CREATE PRODUCT (EXISTS)", product_service.create_product(
    name="Protein Bar",
    unit="Stück",
    price=2.99,
    description="Duplicate test",
    stock=10
)))

# Neues Produkt erfolgreich anlegen
results.append(("CREATE PRODUCT (NEW)", product_service.create_product(
    name="Protein Cookie",
    unit="Stück",
    price=3.49,
    description="Keks mit Protein",
    stock=25
)))

# Produkt mit ID 2 abrufen
product = product_service.get_product_by_id(2)
results.append(("GET PRODUCT BY ID", product.name if not isinstance(product, tuple) else product))

# Produkt aktualisieren
results.append(("UPDATE PRODUCT", product_service.update_product(
    product_id=2,
    price=3.99,
    stock=30
)))

# Nicht vorhandenes Produkt aktualisieren
results.append(("UPDATE NON-EXISTENT PRODUCT", product_service.update_product(
    product_id=9999,
    price=1.99
)))

# Produkt löschen
results.append(("DELETE PRODUCT", product_service.delete_product(2)))

# Nicht vorhandenes Produkt löschen
results.append(("DELETE NON-EXISTENT PRODUCT", product_service.delete_product(9999)))

# ----------- 🧪 USER-TESTS ------------

# Neuen User anlegen
results.append(("CREATE USER", user_service.create_user(
    first_name="Max",
    last_name="Mustermann",
    email="max@test.de",
    phone_number="0123456789",
    address="Musterstraße 1",
    zip_code=12345,
    city="Musterstadt"
)))

# User mit gleicher E-Mail erneut anlegen (sollte Fehler 409 geben)
results.append(("CREATE DUPLICATE USER", user_service.create_user(
    first_name="Max",
    last_name="Mustermann",
    email="max@test.de",
    phone_number="0123456789",
    address="Musterstraße 1",
    zip_code=12345,
    city="Musterstadt"
)))

# User mit ID 1 abrufen
user = user_service.get_user_by_id(1)
results.append(("GET USER BY ID", user.email if not isinstance(user, tuple) else user))

# User aktualisieren
results.append(("UPDATE USER", user_service.update_user(1, city="Teststadt", is_admin=True)))

# Nicht vorhandenen User aktualisieren
results.append(("UPDATE NON-EXISTENT USER", user_service.update_user(9999, city="Nope")))

# User löschen
results.append(("DELETE USER", user_service.delete_user(1)))

# Nicht vorhandenen User löschen
results.append(("DELETE NON-EXISTENT USER", user_service.delete_user(9999)))

# ----------- 🔍 ERGEBNISSE AUSGEBEN ------------
print("\nTEST RESULTS:")
for label, result in results:
    print(f"{label}:\n  → {result}\n")
