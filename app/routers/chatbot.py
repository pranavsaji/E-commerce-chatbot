from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chatbot_service import ChatbotService
from app.utils.preprocess import preprocess_products
from dotenv import load_dotenv
import os
load_dotenv()
# Define request model without `top_k`
class ChatbotQuery(BaseModel):
    query: str
    history: list[str] = []

router = APIRouter()

# Initialize ChatbotService

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Fetch from environment
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
    

chatbot_service = ChatbotService(GEMINI_API_KEY)

# Preprocess and load product data
product_data, product_metadata = preprocess_products("datasets/products.csv")
chatbot_service.rag_service.load_documents(product_data["description"].dropna().tolist(), product_metadata)

@router.post("/query")
def chatbot_query(request: ChatbotQuery):
    """
    Handle chatbot queries with JSON body input.
    """
    query = request.query
    top_k = 5  # Default value for top_k

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    try:
        # Retrieve relevant context using RAG
        context = chatbot_service.rag_service.retrieve(query, top_k=top_k)

        # Generate response using Gemini
        response = chatbot_service.generate_response(query, context)
        return {"query": query, "response": response}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/chat")
def chatbot_query(request: ChatbotQuery):
    """
    Handle chatbot queries with JSON body input.
    """
    query = request.query
    history = request.history or []

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Generate response
    context = chatbot_service.rag_service.retrieve(query, top_k=5)
    response = chatbot_service.generate_response(query, context)
    return {"query": query, "response": response, "history": history + [f"User: {query}", f"Chatbot: {response}"]}

@router.post("/products/chat")
def product_chat(request: ChatbotQuery):
    """
    Handle chatbot queries related to products with conversation history.
    """
    query = request.query
    history = request.history or []

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        # Retrieve relevant context using RAG
        context = chatbot_service.rag_service.retrieve(query, top_k=5)

        # Prepare conversation history for the prompt
        history_str = "\n".join(history)
        prompt = (
            f"You are an expert e-commerce assistant. Your goal is to provide professional, "
            f"and user-friendly responses to queries about products and recommendations. "
            f"Make it concise and to the point including all details "
            f"if you dont have exact information, give an educated guess"
            f"Respond based on the context and conversation history.\n\n"
            f"Conversation History:\n{history_str}\n\n"
            f"User Query: {query}\n\n"
            f"Chatbot Response:"
        )

        # Generate response using Gemini
        response = chatbot_service.gemini_service.generate_response(query, context)

        # Append the new query and response to the history
        updated_history = history + [f"User: {query}", f"Chatbot: {response}"]

        return {
            "query": query,
            "response": response,
            "history": updated_history
        }
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
