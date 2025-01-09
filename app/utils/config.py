import os

class Config:
    PRODUCTS_FILE = os.getenv("PRODUCTS_FILE", "datasets/products.csv")
    ORDERS_FILE = os.getenv("ORDERS_FILE", "datasets/orders.csv")
