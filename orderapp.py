from fastapi import FastAPI
from order_endpoints import router

app = FastAPI(title="Order Dataset API", description="API for querying order-related data")

# Include endpoints
app.include_router(router)
