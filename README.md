# Documentation Interrogation Chatbot-DAFC

## Overview

Chatbot-DAFC is a tool designed to help users find and extract information investigation documentation stocke in a dataset.\
The interface allows users to ask questions and receive relevant, accurate and consist responses based on the content of the documentation.\
*A specific type of documentation has been indexed*


### Prerequisites

- Python 3.12.3
- pip (Python package installer)
- Azure account and services API keys (Azure OpenAI, BlobStorage, Azure Search)

### Steps

1. Clone the repository:
   ```bash
   git clone https://orano@dev.azure.com/orano/ChatBot%20DAFC/_git/ChatBot%20DAFC
   ```
2. Create and activate virtual environment
   ```bash
   python -m venv <env-name>
   .<env-name>/Scripts/Activate.ps1
   ```

3. Install requirements file
	```bash
   pip install -r requirements.txt
   ```
4. Initialize API keys in a new .env file
	```bash
# Chat model
AZURE_OPENAI_API_KEY=<API_key>
AZURE_OPENAI_DEPLOYMENT_ID=<endpoint>
AZURE_OPENAI_ENDPOINT=https://<endpoint>.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=<deployement_name>
AZURE_OPENAI_MODEL=<model>
AZURE_OPENAI_VERSION=<version>
# ------------------------------------------------------------------------------------------------
# Embedding model 
AZURE_OPENAI_EMB_API_KEY=<API_key>
AZURE_OPENAI_EMB_ENDPOINT=https://<endpoint>.openai.azure.com/
AZURE_OPENAI_EMB_DEPLOYMENT_ID=<endpoint>
AZURE_OPENAI_EMB_DEPLOYMENT_NAME=<deployement_name>
AZURE_OPENAI_EMB_MODEL=<model>
AZURE_OPENAI_EMB_VERSION=<version>
# ------------------------------------------------------------------------------------------------
# Azure Blob-Storage
AZURE_STORAGE_API_KEY=<API_key>
AZURE_STORAGE_DEPLOYEMENT_ID=<endpoint>
AZURE_STORAGE_ENDPOINT=https://<endpoint>.blob.core.windows.net/
AZURE_STORAGE_CONTAINER_NAME=<your_container_name>
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName<endpoint>;AccountKey=<API_key>;EndpointSuffix=core.windows.net"
# ------------------------------------------------------------------------------------------------
# Azure AI-Search
AZURE_AI_SEARCH_API_KEY=<API_key>
AZURE_AI_SEARCH_ENDPOINT=https://<endpoint>.search.windows.net/
AZURE_AI_SEARCH_DEPLOYEMENT_ID=f<endpoint>
AZURE_AI_SEARCH_SERVICE_NAME=<endpoint>
AZURE_AI_SEARCH_INDEX_NAME=<your_index_name>
AZURE_AI_SEARCH_INDEXER_NAME=<your_indexer_name>
   ```
5. Prepare data in order to be able to interrogate documentation
	```bash
 	from data_manager import DataPreparationManager
 	data_preparation_manager = DataPreparationManager()
 	data_preparation_manager.download_and_prepare_data()
   ```
6. Open interface and Run API
	```bash
		uvicorn main:app --reload
 		start .\interface.html
   ```
