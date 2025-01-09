import requests
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"


    def generate_response(self, query, context, history=None):
        """
        Generate a response using the Gemini API with prompt engineering.
        """
        system_prompt = (
            "You are an expert e-commerce assistant. Your goal is to provide detailed, professional, "
            "and user-friendly responses to queries about products and recommendations. "
            "Make the respond crisp and to the point and help the users with the products and clarify their doubts"
            "Address them professionally when giving details"
            "Respond based on the provided context and conversation history."
        )

        # Combine query, context, and history into the prompt
        context_str = "\n".join([
            f"Result {i+1}:\n"
            f"Main Category: {doc['metadata'].get('main_category', 'N/A')}\n"
            f"Title: {doc['metadata'].get('title', 'N/A')}\n"
            f"Average Rating: {doc['metadata'].get('average_rating', 'N/A')}\n"
            f"Rating Count: {doc['metadata'].get('rating_number', 'N/A')}\n"
            f"Description: {doc['description']}\n"
            
            for i, doc in enumerate(context)
        ])

        history_str = "\n".join(history) if history else ""

        prompt = (
            f"{system_prompt}\n\n"
            f"Conversation History:\n{history_str}\n\n"
            f"Context:\n{context_str}\n\n"
            f"User Query: {query}\n\n"
            f"Chatbot Response:"
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response generated.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error communicating with Gemini API: {e}")
            return "An error occurred while generating the response."












