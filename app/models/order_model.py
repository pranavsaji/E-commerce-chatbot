from pydantic import BaseModel
from typing import Optional

class Order(BaseModel):

    Order_Date: Optional[str] = None
    Time: Optional[str] = None
    Aging: Optional[float] = 0.0
    Customer_Id: int
    Gender: Optional[str] = "Unknown"
    Device_Type: Optional[str] = "Unknown"
    Customer_Login_type: Optional[str] = "Unknown"
    Product_Category: str
    Product: Optional[str] = "Unknown"
    Sales: float
    Quantity: Optional[int] = 0
    Discount: Optional[float] = 0.0
    Profit: Optional[float] = 0.0
    Shipping_Cost: float
    Order_Priority: Optional[str] = "Unknown"
    Payment_Method: Optional[str] = "Unknown"
