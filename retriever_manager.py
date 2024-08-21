import os
from langchain_community.retrievers import AzureAISearchRetriever

class ManagerRetrieve:
    def __init__(self):
        """
        Initializes the ManagerRetrieve with the AzureAISearchRetriever.
        Raises exceptions if there is an issue with the environment variable or initialization.
        """
        try:
            # Get the index name from environment variables
            self.index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
            # Initialize the retriever
            self.retriever_instance = self.create_retriever()
        except Exception as e:
            raise InitializationError(f"Failed to initialize ManagerRetrieve: {str(e)}")

    def create_retriever(self):
        """
        Creates an AzureAISearchRetriever instance.

        :return: An instance of AzureAISearchRetriever.
        :raises ValueError: If the index_name is invalid or not set.
        """
        if not self.index_name:
            raise ValueError("Index name cannot be empty.")
        
        return AzureAISearchRetriever(
            index_name=self.index_name,
            content_key="content",
            top_k=30
        )

    def get_retriever(self):
        """
        Returns the AzureAISearchRetriever instance.

        :return: AzureAISearchRetriever instance.
        """
        return self.retriever_instance
