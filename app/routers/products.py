

from fastapi import APIRouter, Query
from app.services.rag_service import RAGService
from app.utils.preprocess import preprocess_products

router = APIRouter()
rag_service = RAGService()



# Load product data
product_data, product_metadata = preprocess_products('datasets/products.csv')
rag_service.load_documents(product_data['description'].dropna().tolist(), product_metadata)



@router.get("/query")
def query_products(query: str, top_k: int = Query(5, ge=1, le=10)):
    """Retrieve product details using RAG."""
    try:
        results = rag_service.retrieve(query, top_k=top_k)
        formatted_results = []
        for result in results:
            # Clean up description
            description = result["description"]
            if isinstance(description, list):
                description = " ".join(description)  
            description = description.replace("['", "").replace("']", "").replace("[\"", "").replace("\"]", "") 
            description = (description[:200] + "...") if len(description) > 200 else description  


            formatted_results.append({
                "title": result["metadata"].get("title", "No Title"),
                "description": description,
                "price": result["metadata"].get("price", "Price not available"),
                "rating": result["metadata"].get("average_rating", "N/A")
            })
        return {"query": query, "results": formatted_results}
    except ValueError as e:
        return {"error": str(e)}
