import json
from AzureSearch import AzureSearchService
from VectorQuery import AzureSearchQuery
from RAG import AzureOpenAIClient

class Chatbot:
    def __init__(self):
        self.json_file_path = "C:\\Users\\gciprianherrera\\Desktop\\LLM\\MVP_Chatbot\\MVP_final\\Documents_modele_example\\docs_with_embeddings.json"
        self.azure_search_service = AzureSearchService()
        self.azure_search_query = AzureSearchQuery()
        self.azure_openai_client = AzureOpenAIClient()
        self.docs_with_embeddings = None
    
    def read_json_file(self):
        """Read the JSON file and store the contents in the instance variable."""
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            self.docs_with_embeddings = json.load(f)
        return self.docs_with_embeddings
    
    def upload_documents(self):
        """Upload documents to Azure Search Service."""
        if self.docs_with_embeddings is None:
            self.read_json_file()
        result = self.azure_search_service.upload_documents(self.docs_with_embeddings)
        return result
    
    def perform_vectorized_query(self, query):
        """Perform a vectorized query using the Azure Search Query."""
        input_text = self.azure_search_query.vectorized_query(query)
        return input_text
    
    def ask(self, query):
        """Generate a response using the Azure OpenAI Client based on the vectorized query."""
        input_text = self.perform_vectorized_query(query)
        prompt = f"""En utilisant le context suivant : {input_text}\n 
                il faut repondre de maniere courte et precise avec un maximum de 50 motsa la question suivante seulement en francais: {query}\n
                """
        response = self.azure_openai_client.get_response(prompt)
        return response


