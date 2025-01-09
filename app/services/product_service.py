import pandas as pd

class ProductService:
    def __init__(self):
        self.products = pd.read_csv('datasets/products.csv').fillna("")

    def get_all_products(self):
        """Return all products."""
        return self.products
