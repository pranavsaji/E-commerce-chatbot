from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    Product_ID: int
    Title: str
    Description: str
    Features: Optional[str] = None
    Ratings: float
    Price: float
    Category: str
