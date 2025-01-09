from app.services.rag_service import RAGService
from app.services.gemini_service import GeminiService

class ChatbotService:
    def __init__(self, api_key):
        self.rag_service = RAGService()
        self.gemini_service = GeminiService(api_key)

    def generate_response(self, query, context):
        """
        Generate a chatbot response by integrating RAG and Gemini API.
        :param query: User query
        :param context: Retrieved context (from RAG)
        :return: Gemini-generated response
        """
        return self.gemini_service.generate_response(query, context)
