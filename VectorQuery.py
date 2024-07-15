import os
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
AZURE_AI_SEARCH_API_KEY = os.getenv("AZURE_AI_SEARCH_API_KEY")
AZURE_AI_SEARCH_ENDPOINT = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
AZURE_AI_SEARCH_DEPLOYMENT_ID = os.getenv("AZURE_AI_SEARCH_DEPLOYMENT_ID")
AZURE_AI_SEARCH_INDEX_NAME = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
AZURE_AI_SEARCH_INDEXER_NAME = os.getenv("AZURE_AI_SEARCH_INDEXER_NAME")

class AzureSearchQuery:
    def __init__(self):
        # Initialize the AzureOpenAI client
        self.embedder_model = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_EMB_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_EMB_API_KEY"),
            api_version="2023-05-15",
            azure_deployment=os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT_NAME")
        )

        # Initialize the Azure Search client
        self.search_client = SearchClient(
            endpoint=AZURE_AI_SEARCH_ENDPOINT,
            index_name=AZURE_AI_SEARCH_INDEX_NAME,
            credential=AzureKeyCredential(AZURE_AI_SEARCH_API_KEY)
        )

    def get_embeddings(self, text):
        # Generate embeddings for the provided text
        embeddings = self.embedder_model.embeddings.create(
            input=text,
            # model="text-embedding-3-large",
            model="text-embedding-ada-002"
        )
        return embeddings.data[0].embedding

    # def vectorized_query(self, query, k_nearest_neighbors=20, fields="embeddings", query_language="fr-fr"):
    def vectorized_query(self, query, k_nearest_neighbors=20, fields="embeddings"):
        # Generate the embedding for the query
        query_embedding = self.get_embeddings(query)

        # Create the vector query
        vector_query = VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=k_nearest_neighbors,
            fields=fields
        )

        # Execute the search
        results = self.search_client.search(
            vector_queries=[vector_query],
            select=["page_content"],
            # query_language=query_language
        )

        # Aggregate the results
        input_text = ''
        try:
            while True:
                result = results.next()
                input_text += result["page_content"] + "\n"
        except StopIteration:
            pass

        return input_text