import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

class AzureOpenAIClient:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        # token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
        # Initialize the AzureOpenAI client
        self.completion_client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2023-05-15",
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"), 
            # azure_ad_token_provider=token_provider
        )

    def get_response(self, prompt):
        # Get response from the model
        response = self.completion_client.completions.create(
            model="gpt-35-turbo",
            prompt=prompt,
            temperature=0,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop = [' END']
        )
        # Return the text of the first choice
        # return response.choices[0].text
        return (response.choices[0].text).strip()