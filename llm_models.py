import os
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

class AzureOpenAIManager:
    def __init__(self):
        """
        Initializes the AzureOpenAIManager with environment variables.
        """
        self.llm = self.create_chat()
        self.embeddings = self.create_embeddings()

    def create_chat(self) -> AzureChatOpenAI:
        """
        Creates and returns an AzureChatOpenAI instance.
        
        :return: An instance of AzureChatOpenAI configured with Azure OpenAI details.
        """
        return AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            model=os.getenv("AZURE_OPENAI_MODEL"),
            temperature=0,
        )

    def create_embeddings(self) -> AzureOpenAIEmbeddings:
        """
        Creates and returns an AzureOpenAIEmbeddings instance.
        
        :return: An instance of AzureOpenAIEmbeddings configured with Azure OpenAI details.
        """
        # Load environment variables for embeddings
        azure_openai_emb_endpoint = os.getenv("AZURE_OPENAI_EMB_ENDPOINT")
        azure_openai_emb_api_key = os.getenv("AZURE_OPENAI_EMB_API_KEY")
        azure_openai_emb_version = os.getenv("AZURE_OPENAI_EMB_VERSION")
        azure_openai_emb_deployment_name = os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT_NAME")

        # Initialize and return Azure OpenAI embeddings
        return AzureOpenAIEmbeddings(
            azure_endpoint=azure_openai_emb_endpoint,
            api_key=azure_openai_emb_api_key,
            openai_api_version=azure_openai_emb_version,
            azure_deployment=azure_openai_emb_deployment_name
        )
        
# Example:
# Model = AzureOpenAIManager()
# embeddings = Model.create_embeddings()