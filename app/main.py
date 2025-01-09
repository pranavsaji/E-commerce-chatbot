from fastapi import FastAPI
from app.routers import products, orders, healthcheck, chatbot

app = FastAPI(
    title="E-Commerce Chatbot API",
    description="A scalable chatbot for e-commerce use cases.",
    version="1.0.0"
)


# Include routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(healthcheck.router, prefix="/health", tags=["Healthcheck"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"]) 

