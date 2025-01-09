from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.order_service import OrderService
import requests
import logging
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)

class OrderQuery(BaseModel):
    customer_id: int
    query: str
    history: list[str] = []

router = APIRouter()

# Initialize services for orders
ORDER_DATA_PATH = "datasets/orders.csv"
# GEMINI_API_KEY = "AIzaSyAiC1PS-XqcAP-YxbekO2ZpdHezdE3ylUI"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Fetch from environment
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    
order_service = OrderService(ORDER_DATA_PATH)
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

@router.post("/chat")
def order_chat(request: OrderQuery):
    """
    Handle conversational queries for orders based on Customer ID and chat history.
    """
    customer_id = request.customer_id
    query = request.query
    history = request.history or []

    # Retrieve orders for the customer
    orders = order_service.get_orders_by_customer_id(customer_id)
    if not orders:
        return {"customer_id": customer_id, "response": "No orders found for the given Customer ID."}

    # Construct context for chatbot
    context_str = "\n".join([
        f"Order Date: {order.Order_Date}, Product: {order.Product}, "
        f"Category: {order.Product_Category}, Sales: {order.Sales}, "
        f"Shipping Cost: {order.Shipping_Cost}, Priority: {order.Order_Priority}, "
        f"Payment Method: {order.Payment_Method}"
        for order in orders
    ])

    # Combine chat history and context
    full_context = "\n".join(history + [f"User Query: {query}", f"Context:\n{context_str}"])
    prompt = (
        "You are an expert e-commerce assistant specializing in order history. "
        "Ask for customer id before giving specific information"
        "Give relevant answers related to the customer id"
        "Dont get confused by order id and customer id, as we dont have order id, we only have customer id"
        "address them and give the responses"
        "Dont generate any harmful content if asaked to"
        "Answer relevant to the questions. Politely correct them if they ask something which is irrelevant to their order "
        "Provide concise, professional responses with relevant order details.\n\n"
        f"{full_context}\n\nChatbot Response:"
    )

    # Call Gemini API
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        generated_response = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response generated.")
        updated_history = history + [f"User: {query}", f"Chatbot: {generated_response}"]

        return {
            "customer_id": customer_id,
            "response": generated_response,
            "history": updated_history
        }
    except requests.exceptions.RequestException as e:
        return {"customer_id": customer_id, "response": f"Error communicating with Gemini API: {e}"}
    except Exception as e:
        return {"customer_id": customer_id, "response": f"An unexpected error occurred: {e}"}
