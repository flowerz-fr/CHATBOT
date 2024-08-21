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
4. Dowloading and indexing blob files.
	```bash
   pip install -r requirements.txt
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
