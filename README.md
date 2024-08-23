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
   python
 	from data_manager import DataPreparationManager
 	data_preparation_manager = DataPreparationManager()
 	data_preparation_manager.download_and_prepare_data()
   ```

7. Open interface and Run API
	```bash
	uvicorn main:app --reload
 	start .\interface.html
   ```


### Définitions

1. **storage_manager.py**

| Fonctionnalité                        | Description                                                                                                        |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Initialiser les clients Azure Blob Storage | Établir des connexions avec Azure Blob Storage en utilisant une chaîne de connexion et le nom du conteneur à partir des variables d'environnement. |
| Créer et supprimer des conteneurs       | Créer ou supprimer un conteneur Azure Blob Storage spécifié, en gérant les cas où le conteneur existe déjà ou n'existe pas. |
| Télécharger un répertoire               | Télécharger un répertoire local entier vers la destination spécifiée dans Azure Blob Storage.                      |
| Lister les blobs                        | Lister tous les blobs (fichiers) dans le conteneur spécifié.                                                        |
| Télécharger des blobs                   | Télécharger soit tous les blobs, soit un blob spécifique du conteneur Azure vers un répertoire local.                 |
| Obtenir le chemin du dossier de téléchargement | Récupérer le chemin absolu du dossier local où les fichiers téléchargés sont stockés.                               |

2. **index_manager.py**

| Fonctionnalité                        | Description                                                                                                         |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Initialiser les variables d'environnement | Charger les variables d'environnement, y compris les clés API, le point de terminaison et le nom de l'index pour Azure AI Search. |
| Initialiser SearchIndexClient         | Créer une instance de `SearchIndexClient` pour gérer les index Azure Search en utilisant les informations d'identification fournies. |
| Supprimer un index                    | Supprimer un index existant d'Azure Search.                                                                         |
| Obtenir le nom de l'index              | Récupérer le nom de l'index Azure Search actuel à partir des variables d'environnement.                              |

3. **directory_processor.py**

| Fonctionnalité                        | Description                                                                                                         |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Initialiser DirectoryProcessor       | Définir le répertoire et initialiser une liste de données vide pour stocker les informations des documents traités. |
| Traiter un document                   | Traiter un document unique, extraire les métadonnées et le contenu, et ajouter ces informations sous forme de dictionnaire à la liste interne des données. |
| Traiter un répertoire                 | Parcourir tous les sous-répertoires et fichiers dans le répertoire de départ, traiter chaque document PDF, et retourner les données accumulées sous forme de DataFrame. |

4. **llm_models.py**

| Fonctionnalité                        | Description                                                                                                         |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Initialiser AzureOpenAIManager        | Initialiser le gestionnaire avec les variables d'environnement pour configurer les services Azure OpenAI.           |
| Créer une instance AzureChatOpenAI    | Créer et retourner une instance d'`AzureChatOpenAI`, configurée avec les informations d'identification et les détails Azure OpenAI provenant des variables d'environnement. |
| Créer une instance AzureOpenAIEmbeddings | Créer et retourner une instance d'`AzureOpenAIEmbeddings`, configurée avec les détails Azure OpenAI pour les embeddings en utilisant les variables d'environnement. |

5. **loader_manager.py**

| Fonctionnalité                        | Description                                                                                                         |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Initialiser DocumentLoaderManager     | Initialiser le gestionnaire avec un DataFrame et un nom de colonne spécifié avec le texte à charger.    |
| Charger des documents depuis le DataFrame | Charger des documents depuis le DataFrame. Vérifie si le DataFrame est vide ou si la colonne spécifiée existe avant le chargement.|

6. **splitter_manager.py**

| Fonctionnalité                        | Description                                                                                                         |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Initialiser DocumentSplitter          | Initialiser le `DocumentSplitter` avec les paramètres spécifiés.|
| Diviser des documents                 | Diviser les documents fournis en morceaux plus petits. |

7. **vector_store_manager.py**

| Fonctionnalité                        | Description                                                                                                         |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Initialiser VectorStoreManager        | Charger les variables d'environnement requises pour les configurations d'Azure Search et de l'API OpenAI.          |
| Créer un magasin de vecteurs          | Créer et retourner une instance de vecteurs. |
| Ajouter des documents                | Ajouter une liste de documents au vecteurs.            |

8. **retriever_manager.py**

| Fonctionnalité                        | Description                                                                                                         |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Initialiser ManagerRetrieve           | Initialiser `ManagerRetrieve` avec `AzureAISearchRetriever`, en chargeant le nom de l'index à partir des variables. |
| Créer un récupérateur                 | Créer et retourner une instance d'`AzureAISearchRetriever`, en s'assurant que le nom de l'index est fourni et configuré avec des paramètres spécifiques. |
| Obtenir le récupérateur               | Retourner l'instance d'`AzureAISearchRetriever` pour l'utilisation dans la récupération de documents.|

9. **QA_manager.py**

| Fonctionnalité                        | Description                                                                                                         |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| Initialiser QuestionAnswerManager     | Initialiser `QuestionAnswerManager` avec des instances de `AzureOpenAIManager`, `ManagerRetrieve`, et `PromptManager`. Créer des chaînes pour le traitement et la récupération de documents. |
| Poser une question                   | Traiter une question en utilisant les chaînes initialisées et retourner le résultat sous forme d'un objet JSON.|



