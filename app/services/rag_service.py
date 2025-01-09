

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging
logger = logging.getLogger(__name__)
class RAGService:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.embeddings = None
        self.documents = None

    

    def load_documents(self, documents, metadata):
        """Load documents and create embeddings."""
        if not documents or not isinstance(documents, list) or len(documents) == 0:
            raise ValueError("Documents are empty or invalid.")

        self.documents = [{"description": doc, "metadata": meta} for doc, meta in zip(documents, metadata)]
        descriptions = [doc["description"] for doc in self.documents]

        # Log tokenization and length
        logger.info("Generating embeddings...")
        token_lengths = [len(self.model.tokenize(desc)) for desc in descriptions]
        logger.info(f"Token lengths: {token_lengths}")
        logger.info(f"Total tokens across all documents: {sum(token_lengths)}")

        self.embeddings = self.model.encode(descriptions, convert_to_tensor=False)


    def retrieve(self, query, top_k=5):
        """Retrieve top-k similar documents."""
        logger.debug(f"Received query: {query}")

        if self.documents is None or self.embeddings is None:
            raise ValueError("Documents or embeddings are not initialized. Please call 'load_documents' first.")

        # Encode the query
        query_embedding = self.model.encode(query, convert_to_tensor=False).reshape(1, -1)
        logger.debug(f"Query embedding shape: {query_embedding.shape}")

        # Compute cosine similarity
        scores = cosine_similarity(query_embedding, self.embeddings).flatten()
        logger.debug(f"Cosine similarity scores: {scores}")

        # Get top-k indices
        top_indices = np.argsort(scores)[-top_k:][::-1]
        logger.debug(f"Top indices: {top_indices}")

        # Fetch top-k documents (with metadata)
        results = [self.documents[i] for i in top_indices]
        logger.debug(f"Top results: {results}")
        return results
    
