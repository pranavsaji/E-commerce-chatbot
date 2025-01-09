from fastapi import APIRouter, HTTPException
import pandas as pd

# Initialize the router
router = APIRouter()

# Load dataset
DATASET_PATH = "datasets/orders.csv"
df = pd.read_csv(DATASET_PATH)

# Clean data
df.fillna(value="", inplace=True)

# Endpoint to get all data
@router.get("/data")
def get_all_data():
    """Retrieve all records in the dataset."""
    return df.to_dict(orient="records")

# Endpoint to filter data by Customer ID
@router.get("/data/customer/{customer_id}")
def get_customer_data(customer_id: int):
    """Retrieve all records for a specific Customer ID."""
    filtered_data = df[df["Customer_Id"] == customer_id]
    if filtered_data.empty:
        return {"error": f"No data found for Customer ID {customer_id}"}
    return filtered_data.to_dict(orient="records")

# Endpoint to filter data by Product Category
@router.get("/data/product-category/{category}")
def get_product_category_data(category: str):
    """Retrieve all records for a specific Product Category."""
    filtered_data = df[df["Product_Category"].str.contains(category, case=False, na=False)]
    if filtered_data.empty:
        return {"error": f"No data found for Product Category '{category}'"}
    return filtered_data.to_dict(orient="records")

# Endpoint to get orders with specific priorities
@router.get("/data/order-priority/{priority}")
def get_orders_by_priority(priority: str):
    """Retrieve all orders with the given priority."""
    filtered_data = df[df["Order_Priority"].str.contains(priority, case=False, na=False)]
    if filtered_data.empty:
        return {"error": f"No data found for Order Priority '{priority}'"}
    return filtered_data.to_dict(orient="records")

# Endpoint to calculate total sales by Product Category
@router.get("/data/total-sales-by-category")
def total_sales_by_category():
    """Calculate total sales by Product Category."""
    sales_summary = df.groupby("Product_Category")["Sales"].sum().reset_index()
    return sales_summary.to_dict(orient="records")

# Endpoint to get high-profit products
@router.get("/data/high-profit-products")
def high_profit_products(min_profit: float = 100.0):
    """Retrieve products with profit greater than the specified value."""
    filtered_data = df[df["Profit"] > min_profit]
    if filtered_data.empty:
        return {"error": f"No products found with profit greater than {min_profit}"}
    return filtered_data.to_dict(orient="records")

# Endpoint to get shipping cost summary
@router.get("/data/shipping-cost-summary")
def shipping_cost_summary():
    """Retrieve the average, minimum, and maximum shipping cost."""
    summary = {
        "average_shipping_cost": df["Shipping_Cost"].mean(),
        "min_shipping_cost": df["Shipping_Cost"].min(),
        "max_shipping_cost": df["Shipping_Cost"].max()
    }
    return summary

# Endpoint to calculate total profit by Gender
@router.get("/data/profit-by-gender")
def profit_by_gender():
    """Calculate total profit by customer gender."""
    profit_summary = df.groupby("Gender")["Profit"].sum().reset_index()
    return profit_summary.to_dict(orient="records")

# Endpoint to get most recent order for a Customer ID
@router.get("/data/most-recent-order/{customer_id}")
def most_recent_order(customer_id: int):
    """Retrieve the most recent order for a given Customer ID."""
    filtered_data = df[df["Customer_Id"] == customer_id].sort_values(by="Order_Date", ascending=False)
    if filtered_data.empty:
        return {"error": f"No data found for Customer ID {customer_id}"}
    return filtered_data.iloc[0].to_dict()

# Endpoint to calculate total profit by Product Category
@router.get("/data/profit-by-category")
def profit_by_category():
    """Calculate total profit by Product Category."""
    profit_summary = df.groupby("Product_Category")["Profit"].sum().reset_index()
    return profit_summary.to_dict(orient="records")

# Endpoint to fetch n most recent high-priority orders
@router.get("/data/high-priority-recent-orders/{n}")
def high_priority_recent_orders(n: int = 5):
    """Retrieve n most recent high-priority orders."""
    filtered_data = df[df["Order_Priority"].str.contains("high", case=False, na=False)].sort_values(by="Order_Date", ascending=False).head(n)
    if filtered_data.empty:
        return {"error": "No high-priority orders found."}
    return filtered_data.to_dict(orient="records")

# Dynamic query handler endpoint
@router.post("/chat")
def dynamic_query_handler(query: str, customer_id: int = None):
    """
    Dynamically handle queries based on query type and optional Customer ID.
    """
    if not customer_id:
        return {"response": "Please provide your Customer ID to proceed."}

    # Sample logic to determine query type
    if "cell-phone order" in query.lower():
        filtered_data = df[(df["Customer_Id"] == customer_id) & (df["Product_Category"].str.contains("cell-phone", case=False, na=False))]
        if filtered_data.empty:
            return {"response": "No orders found for cell phones for the given Customer ID."}
        return {"response": filtered_data.to_dict(orient="records")}

    # Default fallback response
    return {"response": "I'm sorry, I couldn't determine your query. Could you rephrase it?"}
