import os
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential

class IndexManager:
    def __init__(self):
        # Load environment variables
        self.api_key = os.getenv("AZURE_AI_SEARCH_API_KEY")
        self.endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
        self.index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        # Initialize the SearchIndexClient for index management
        
        self.index_client = SearchIndexClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )

    def delete_index(self):
        """
        Delete an index from Azure Search.
        """
        try:
            # Delete the index
            self.index_client.delete_index(self.index_name)
            print(f"Index '{self.index_name}' deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting the index: {str(e)}")

    def get_index_name(self):
        """
        Retrieve the name of the current Azure Search index.

        :return: The name of the index.
        """
        return self.index_name