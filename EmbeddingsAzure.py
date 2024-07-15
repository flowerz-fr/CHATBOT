import os
import uuid
from openai import AzureOpenAI
from dotenv import load_dotenv

class DocumentEmbedderAzure:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize the AzureOpenAI client
        self.embedder_model = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_EMB_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_EMB_API_KEY"),
            api_version="2023-05-15",
            azure_deployment=os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT_NAME")
        )

    def get_embeddings(self, text):
        # Generate embeddings for the provided text
        embeddings = self.embedder_model.embeddings.create(
            input=text,
            # model="text-embedding-3-large",
            model="text-embedding-ada-002"
        )
        return embeddings.data[0].embedding

    def create_document_embeddings(self, documents):
        # Process a list of documents and generate embeddings
        embedded_docs = []
        for doc in documents:
            # print number of documents processed so far
            # print(f"Processing document {len(embedded_docs)+1}/{len(documents)}")
            embedded_docs.append({
                "id": str(doc['id']),
                "page_content": doc['page_content'],
                "embeddings": self.get_embeddings(doc['page_content']),
                "Perimeter": doc['Perimeter'],
                "Title": doc['Title'],
                "Version": doc['Version'],
                "Date": doc['Date'],
            })
        return embedded_docs