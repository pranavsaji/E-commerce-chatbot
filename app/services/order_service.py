import pandas as pd
from app.models.order_model import Order

class OrderService:
    def __init__(self, order_data_path):
        # Load order data from the CSV file
        self.order_data = pd.read_csv(order_data_path)
        self.validate_columns()

    def validate_columns(self):
        """
        Ensure all required columns are present in the dataset. Add missing columns with default values.
        """
        required_columns = [
            "Order_Date", "Time", "Aging", "Customer_Id", "Gender", "Device_Type",
            "Customer_Login_type", "Product_Category", "Product", "Sales",
            "Quantity", "Discount", "Profit", "Shipping_Cost", "Order_Priority", "Payment_method"
        ]
        for column in required_columns:
            if column not in self.order_data.columns:
                self.order_data[column] = "Unknown" if column not in ["Sales", "Quantity", "Discount", "Profit", "Shipping_Cost", "Aging"] else 0.0

    def get_orders_by_customer_id(self, customer_id):
        """
        Retrieve all orders for a given customer ID.
        """
        customer_orders = self.order_data[self.order_data["Customer_Id"] == customer_id].copy()
        if customer_orders.empty:
            return []

        customer_orders.fillna({
            "Order_Date": "Unknown",
            "Time": "Unknown",
            "Aging": 0.0,
            "Gender": "Unknown",
            "Device_Type": "Unknown",
            "Customer_Login_type": "Unknown",
            "Product_Category": "Unknown",
            "Product": "Unknown",
            "Sales": 0.0,
            "Quantity": 0,
            "Discount": 0.0,
            "Profit": 0.0,
            "Shipping_Cost": 0.0,
            "Order_Priority": "Unknown",
            "Payment_Method": "Unknown"
        }, inplace=True)

        return [Order(**row) for row in customer_orders.to_dict(orient="records")]
