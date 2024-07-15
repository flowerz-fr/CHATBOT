import os
from semantic_router.encoders import OpenAIEncoder
from semantic_chunkers import StatisticalChunker
import pandas as pd
from openai import AzureOpenAI

class DatasetChunker:
    def __init__(self):
        self.encoder = self.initialize_encoder()
        self.chunker = self.create_chunker(self.encoder)
    
    # def initialize_encoder(self):
    #     # Set the OpenAI API key from environment variable
    #     os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    #     # Initialize the encoder
    #     encoder = OpenAIEncoder(name="text-embedding-ada-002")
    #     return encoder
    
    
    
    def initialize_encoder(self):
        # Set the OpenAI API key from environment variable
        # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        azure_endpoint=os.getenv("AZURE_OPENAI_EMB_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_EMB_API_KEY"),
        api_version="2023-05-15",
        azure_deployment=os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT_NAME")
        # Initialize the encoder
        encoder = OpenAIEncoder(name="text-embedding-ada-002")
        return encoder

    def create_chunker(self, encoder):
        return StatisticalChunker(encoder=encoder)

    def process_dataset(self, data):
        all_record_metadata = []

        for idx, document in data.iterrows():
            record_texts = self.chunker([document['page_content']])
            processed_texts = []
            for chunk in record_texts[0]:
                text_chunk = chunk.splits
                text_chunk = " ".join(text_chunk)
                processed_texts.append(text_chunk)

            metadata = {
                'Title': document['Title'],
                'Version': document['Version'],
                'Date': document['Date'],
                'Confidentiality': document['Confidentiality'],
                'Perimeter': document['Perimeter'],
                'Investigation Number': document['Investigation Number'],
                'Source': document['Source'],
            }

            record_metadata = [{"chunk": j, "page_content": text, **metadata} for j, text in enumerate(processed_texts)]
            all_record_metadata.extend(record_metadata)

        return all_record_metadata