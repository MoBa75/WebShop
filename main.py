from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
from fastapi.openapi.utils import get_openapi

# Routers (angepasste Importe)
from app.web.web_routes import router as web_router
from app.user.user_routes import router as user_router
from app.product.product_routes import router as product_router
from app.order.order_routes import router as order_router
from app.admin.admin_routes import router as admin_router  # aktiviert

# Load environment variables
load_dotenv()

app = FastAPI()

# Include Routers
app.include_router(web_router)
app.include_router(user_router, prefix="/api/users")
app.include_router(product_router, prefix="/api/products")
app.include_router(order_router, prefix="/api/orders")
app.include_router(admin_router)  # Prefix ist bereits in der Datei gesetzt

# Custom OpenAPI Schema for Auth0 Integration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Webshop API",
        version="1.0.0",
        description="Secure Webshop API with Auth0 Integration",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Entry point for development
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5002, reload=True)
