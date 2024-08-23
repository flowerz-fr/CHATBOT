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
2. Sing in axure account
   ```bash
   Azure:Sign in
   ```
3. Create and activate virtual environment
   ```bash
   # In windows
   python -m venv <venv-name>
   .<env-name>/Scripts/Activate.ps1
   ```

4. Install requirements file
	```bash
   pip install -r requirements.txt
   ```
5. Initialize API keys in a new .env file
	```bash
   # Chat model
   AZURE_OPENAI_API_KEY=<API_key>
   AZURE_OPENAI_DEPLOYMENT_ID=<deployement_id>
   AZURE_OPENAI_ENDPOINT=https://<deployement_id>.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=<deployement_name>
   AZURE_OPENAI_MODEL=<model>
   AZURE_OPENAI_VERSION=<version>
   # ------------------------------------------------------------------------------------------------
   # Embedding model 
   AZURE_OPENAI_EMB_API_KEY=<API_key>
   AZURE_OPENAI_EMB_DEPLOYMENT_ID=<deployement_id>
   AZURE_OPENAI_EMB_ENDPOINT=https://<deployement_id>.openai.azure.com/
   AZURE_OPENAI_EMB_DEPLOYMENT_NAME=<deployement_name>
   AZURE_OPENAI_EMB_MODEL=<model>
   AZURE_OPENAI_EMB_VERSION=<version>
   # ------------------------------------------------------------------------------------------------
   # Azure Blob-Storage
   AZURE_STORAGE_API_KEY=<API_key>
   AZURE_STORAGE_DEPLOYEMENT_ID=<deployement_id>
   AZURE_STORAGE_ENDPOINT=https://<deployement_id>.blob.core.windows.net/
   AZURE_STORAGE_CONTAINER_NAME=<your_container_name>
   AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName<endpoint>;AccountKey=<API_key>;EndpointSuffix=core.windows.net"
   # ------------------------------------------------------------------------------------------------
   # Azure AI-Search
   AZURE_AI_SEARCH_API_KEY=<API_key>
   AZURE_AI_SEARCH_DEPLOYEMENT_ID=<deployement_id>
   AZURE_AI_SEARCH_ENDPOINT=https://<deployement_id>.search.windows.net/
   AZURE_AI_SEARCH_SERVICE_NAME=<endpoint>
   AZURE_AI_SEARCH_INDEX_NAME=<your_index_name>
   AZURE_AI_SEARCH_INDEXER_NAME=<your_indexer_name>
   ```
6. Prepare data in order to be able to interrogate documentation
	```bash
 	from data_manager import DataPreparationManager
 	data_preparation_manager = DataPreparationManager()
 	data_preparation_manager.download_and_prepare_data()
   ```

7. Open interface and Run API
	```bash
	uvicorn main:app --reload
 	start .\interface.html
   ```


## Definitions 

1.  storage_manager.py

| **Functionality**                  | **Description**                                                                                       |
|------------------------------------|-------------------------------------------------------------------------------------------------------|
| Initialize Azure Blob Storage Clients | Establish connections to Azure Blob Storage using a connection string and container name from environment variables. |
| Create and Delete Containers        | Create or delete a specified Azure Blob Storage container, handling cases where the container already exists or does not exist. |
| Upload a Directory                  | Upload an entire local directory to the specified destination in Azure Blob Storage.                 |
| List Blobs                          | List all blobs (files) within the specified container.                                               |
| Download Blobs                      | Download either all blobs or a specific blob from the Azure container to a local directory.          |
| Get Download Folder Path            | Retrieve the absolute path of the local folder where downloaded files are stored.                   |


