import os
import uuid
from openai import OpenAI
from getpass import getpass

class DocumentEmbedder:
    def __init__(self, api_key=None):
        # Set the OpenAI API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or getpass("OpenAI API key: ")
        os.environ["OPENAI_API_KEY"] = self.api_key
        
        # Initialize the OpenAI client
        self.client_emb = OpenAI()

    def get_embeddings(self, text):
        # Generate embeddings for the provided text
        embeddings = self.client_emb.embeddings.create(
            input=text,
            # model="text-embedding-3-large",
            model="text-embedding-ada-002"
        )
        return embeddings.data[0].embedding

    def create_document_embeddings(self, documents):
        # Process a list of documents and generate embeddings
        embedded_docs = []
        for doc in documents:
            embedded_docs.append({
                "id": str(uuid.uuid4()),
                "page_content": doc['page_content'],
                "embeddings": self.get_embeddings(doc['page_content']),
                "Perimeter": doc['Perimeter'],
                "Title": doc['Title'],
                "Version": doc['Version'],
                "Date": doc['Date'],
            })
        return embedded_docs