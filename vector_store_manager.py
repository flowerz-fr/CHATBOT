from langchain_community.vectorstores.azuresearch import AzureSearch
from llm_models import AzureOpenAIManager
import os

class VectorStoreManager:
    def __init__(self):
        # Load environment variables
        self.api_key = os.getenv("AZURE_AI_SEARCH_API_KEY")
        self.endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
        self.index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def create_vector_store(self) -> AzureSearch:
        """
        Creates and returns an AzureSearch vector store using Azure OpenAI embeddings.
        """
        # Create embeddings instance
        embeddings_manager = AzureOpenAIManager()
        embeddings = embeddings_manager.create_embeddings()

        # Create and return the AzureSearch vector store
        vector_store = AzureSearch(
            azure_search_key=self.api_key,
            azure_search_endpoint=self.endpoint,
            index_name=self.index_name,
            embedding_function=embeddings.embed_query
        )
        return vector_store

    def add_documents(self, documents):
        """
        Adds documents to the AzureSearch vector store.

        :param documents: A list of documents to be added to the vector store.
        :raises RuntimeError: If an error occurs while adding documents.
        """
                
        try:
            # Get the vector store
            vector_store = self.create_vector_store()

            # Add documents to the vector store
            vector_store.add_documents(documents=documents)
            print("Documents added successfully.")
        except Exception as e:
            raise RuntimeError(f"An error occurred while adding documents: {str(e)}")
