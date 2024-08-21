from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError
import os
from upload_files_folder_to_blob import DirectoryClient

class AzureBlobStorageManager:
    def __init__(self):
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        
        # The folder where the downloaded files will be stored
        self.container_files = "downloaded_files"
        
        # Ensure the connection string is correctly formatted
        if not self.connection_string.startswith("DefaultEndpointsProtocol="):
            self.connection_string = "DefaultEndpointsProtocol=" + self.connection_string
        
        # Initialize BlobServiceClient and ContainerClient
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        self.directory_client = DirectoryClient(self.connection_string, self.container_name)

    def create_container(self):
        try:
            if not self.container_client.exists():
                self.container_client.create_container()
                print(f"Container with the name '{self.container_name}' has been created")
            else:
                print(f"Container with the name '{self.container_name}' already exists")
        except ResourceExistsError:
            print(f"A container with the name '{self.container_name}' already exists")

    def delete_container(self):
        try:
            if self.container_client.exists():
                self.container_client.delete_container()
                print(f"Container with the name '{self.container_name}' has been deleted")
            else:
                print(f"Container with the name '{self.container_name}' does not exist")
        except Exception as e:
            print(f"An error occurred while trying to delete the container: {str(e)}")

    def upload_directory(self, source=None, destination="", local_folder=""):
        try:
            if source is None:
                source = os.path.join(os.getcwd(), local_folder)
            
            if not os.path.exists(source):
                print(f"The source directory '{source}' does not exist.")
                return
            
            # Upload the directory
            self.directory_client.upload_dir(source, destination)
            print(f"Directory '{source}' has been uploaded to '{destination}'")
        
        except Exception as e:
            print(f"An error occurred while uploading the directory: {str(e)}")

    def list_blobs_flat(self):
        try:
            # List all blobs in the container
            blob_list = self.container_client.list_blobs()

            # Print the names of the blobs
            for blob in blob_list:
                print(f"Name: {blob['name']}")
        
        except Exception as e:
            print(f"An error occurred while listing blobs: {str(e)}")

    def download_blobs(self, blob_name: str = None):
        try:
            # Determine whether to download a single blob or all blobs
            blob_list = [blob_name] if blob_name else [blob.name for blob in self.container_client.list_blobs()]

            for blob in blob_list:
                # Get blob client
                blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob)
                
                # Determine file name and subfolder
                file_name = blob.split("/")[-1]
                subfolder = blob.split("/")[-2] if '/' in blob else ''
                folder_path = os.path.join(self.container_files, subfolder)
                
                # Create subfolder if it does not exist
                os.makedirs(folder_path, exist_ok=True)
                
                # Construct file path
                file_path = os.path.join(folder_path, file_name)
                
                # Check if file already exists
                if os.path.exists(file_path):
                    print(f"File already exists: {file_path}")
                    continue
                
                # Download blob to file
                with open(file_path, mode="wb") as sample_blob:
                    download_stream = blob_client.download_blob()
                    sample_blob.write(download_stream.readall())
                
                print(f"Downloaded to: {file_path}")
        except Exception as e:
            print(f"An error occurred while downloading blobs: {str(e)}")
            
    def get_download_folder_path(self):
        return os.path.abspath(self.container_files)

# Example:

# manager = AzureBlobStorageManager() # Initialize the manager
# manager.create_container()  # Create a container
# manager.upload_directory()  # Upload a directory
# manager.list_blobs_flat()   # List blobs in the container
# manager.download_blobs()    # Download all blobs
# manager.download_blobs('specific_blob_name')  # Download a specific blob
# manager.delete_container()  # Delete the container
