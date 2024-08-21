from storage_manager import AzureBlobStorageManager
from directory_processor import DirectoryProcessor
from llm_models import AzureOpenAIManager
from loader_manager import DocumentLoaderManager
from splitter_manager import DocumentSplitter
from vector_store_manager import VectorStoreManager

class DataPreparationManager:
    def __init__(self):
        """
        Initialize the necessary components for data preparation.
        """
        self.blob_storage_manager = AzureBlobStorageManager()
        self.directory_processor = None
        self.embeddings = None

    def download_and_prepare_data(self):
        """
        Executes the full data preparation pipeline, including downloading blobs, 
        processing directories, loading documents, splitting them, and storing vectors.
        """
        # Step 1: Download blobs from Azure Blob Storage
        self.blob_storage_manager.download_blobs()  # Download all blobs
        
        # Step 2: Process the downloaded directory
        download_path = self.blob_storage_manager.get_download_folder_path()
        self.directory_processor = DirectoryProcessor(download_path)
        dataset = self.directory_processor.process_directory()
        
        # Step 3: Create embeddings using Azure OpenAI model
        model = AzureOpenAIManager()
        self.embeddings = model.create_embeddings()
        
        # Step 4: Load documents from the processed dataset
        loader_manager = DocumentLoaderManager(data=dataset, page_content_column="page_content")
        try:
            documents = loader_manager.load_documents_from_dataframe()
        except Exception as e:
            print(f"An error occurred while loading documents: {str(e)}")
            return
        
        # Step 5: Split the loaded documents into manageable chunks
        splitter = DocumentSplitter()
        try:
            splits = splitter.split_documents(documents)
        except Exception as e:
            print(f"An error occurred while splitting documents: {str(e)}")
            return
        
        # Step 6: Store the document chunks in a vector store
        vector_store_manager = VectorStoreManager()
        vector_store_manager.add_documents(splits)
