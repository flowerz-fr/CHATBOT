import os
from azure.search.documents.indexes import SearchIndexClient
import azure.identity
# from azure.search.documents.indexes.models import SearchIndex, SearchFieldDataType, SimpleField, SearchableField, SearchField, VectorSearch, VectorSearchProfile, HnswAlgorithmConfiguration, HnswParameters
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    HnswParameters,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchAlgorithmKind,
    VectorSearchProfile,
    SearchableField
)
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

class AzureSearchService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("AZURE_AI_SEARCH_API_KEY")
        self.endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
        self.index_name = os.getenv("AZURE_AI_SEARCH_INDEX_NAME")
        self.indexer_name = os.getenv("AZURE_AI_SEARCH_INDEXER_NAME")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.index_client = SearchIndexClient(self.endpoint, AzureKeyCredential(self.api_key))
        self.search_client = SearchClient(self.endpoint, index_name=self.index_name, credential=AzureKeyCredential(self.api_key))

    def create_vector_search(self):
        # vector_search = VectorSearch(
        #     profiles=[VectorSearchProfile(name="my-vector-config", algorithm_configuration_name="my-algorithms-config")],
        #     algorithms=[HnswAlgorithmConfiguration(name="my-algorithms-config", parameters={"distanceMeasure": "Cosine"})]
        # )
        vector_search = VectorSearch(
            profiles=[VectorSearchProfile(name="my-vector-config", algorithm_configuration_name="my-algorithms-config")],
            algorithms=[HnswAlgorithmConfiguration(name="my-algorithms-config", kind = VectorSearchAlgorithmKind.HNSW ,parameters=HnswParameters(metric="Cosine"))]
        )
        return vector_search

    def create_search_index(self):
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="page_content", type=SearchFieldDataType.String, analyzer_name="fr.lucene"),
            SearchField(name="embeddings", 
                        type=SearchFieldDataType.Collection(SearchFieldDataType.Single), 
                        searchable=True,
                        vector_search_dimensions=1536,
                        vector_search_profile_name="my-vector-config"),
            SearchableField(name="Perimeter", type=SearchFieldDataType.String, sortable=True, filterable=True),
            SearchableField(name="Title", type=SearchFieldDataType.String, analyzer_name="fr.lucene"),
            SearchableField(name="Version", type=SearchFieldDataType.String, sortable=True, filterable=True),
            SearchableField(name="Date", type=SearchFieldDataType.String, sortable=True, filterable=True),
            SearchableField(name="Source", type=SearchFieldDataType.String, sortable=True, filterable=True),
        ]
        vector_search = self.create_vector_search()
        index = SearchIndex(name=self.index_name, fields=fields, vector_search=vector_search)
        self.index_client.delete_index(index)
        self.index_client.create_index(index)

    def upload_documents(self, docs):
        result = self.search_client.upload_documents(docs)
        return result