from datamanager.product_service import ProductService
from datamanager.postgres_data_manager import PostgresDataManager

data_manager = PostgresDataManager()
product_service = ProductService(data_manager)

result, status_code = product_service.create_product(
    name="Protein Bar",
    unit="Stück",
    price=2.99,
    description="Leckere Eiweißriegel mit 20g Protein",
    stock=50
)

print(f"Status: {status_code}")
print("Antwort:", result)
