# test_product_service.py

from datamanager.product_service import ProductService
from datamanager.postgres_data_manager import PostgresDataManager

# Instanzen initialisieren
data_manager = PostgresDataManager()
product_service = ProductService(data_manager)

print("---- CREATE 1 ----")
result, status = product_service.create_product(
    name="Protein Bar",
    unit="Stück",
    price=2.99,
    description="Eiweißriegel mit 20g Protein",
    stock=50
)
print("Status:", status)
print("Antwort:", result)

print("\n---- CREATE DUPLICATE ----")
result, status = product_service.create_product(
    name="Protein Bar",  # Gleicher Name wie oben
    unit="Stück",
    price=3.49,
    description="Duplikat-Test",
    stock=20
)
print("Status:", status)
print("Antwort:", result)

print("\n---- GET PRODUCT BY ID ----")
product = product_service.get_product_by_id(1)
print("Produkt:", product if isinstance(product, dict) else product.name)

print("\n---- GET ALL PRODUCTS ----")
products = product_service.get_all_products()
if isinstance(products, list):
    for p in products:
        print(f"{p.id}: {p.name} ({p.price} €)")
else:
    print(products)

print("\n---- UPDATE EXISTING PRODUCT ----")
result, status = product_service.update_product(1, price=3.49, stock=60)
print("Status:", status)
print("Antwort:", result)

print("\n---- UPDATE NON-EXISTENT PRODUCT ----")
result, status = product_service.update_product(999, price=9.99)
print("Status:", status)
print("Antwort:", result)

print("\n---- DELETE EXISTING PRODUCT ----")
result, status = product_service.delete_product(1)
print("Status:", status)
print("Antwort:", result)

print("\n---- DELETE NON-EXISTENT PRODUCT ----")
result, status = product_service.delete_product(999)
print("Status:", status)
print("Antwort:", result)
