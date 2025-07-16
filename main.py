from fastapi import FastAPI
import uvicorn

from routes.web_routes import router as web_router
from app.user.user_routes import router as user_router
from app.product.product_routes import router as product_router
from app.order.order_routes import router as order_router
# from routes.admin_routes import router as admin_router

app = FastAPI()

app.include_router(web_router)
app.include_router(user_router, prefix="/api/users")
app.include_router(product_router, prefix="/api/products")
app.include_router(order_router, prefix="/api/orders")
# app.include_router(admin_router, prefix="/admin")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5002, reload=True)
