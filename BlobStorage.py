import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceExistsError
from dotenv import load_dotenv

class AzureBlobStorageDownloader:
    def __init__(self):
        load_dotenv()
        self.connection_string = self._get_connection_string()
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

    def _get_connection_string(self):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string.startswith("DefaultEndpointsProtocol="):
            connection_string = "DefaultEndpointsProtocol=" + connection_string
        return connection_string

    def download_blob_to_file(self, blob_name):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
        file_name = blob_name.split("/")[-1]
        
        # Create a folder name with the -2 element of the blob_name if it does not exist in the downloaded_files folder
        subfolder = blob_name.split("/")[-2]
        os.makedirs(os.path.join('blob_files', subfolder), exist_ok=True)
        
        file_path = os.path.join('blob_files', subfolder, file_name)
        
        # Check if file already exists
        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            return None
        
        with open(file_path, mode="wb") as sample_blob:
            download_stream = blob_client.download_blob()
            sample_blob.write(download_stream.readall())
        
        return file_path

    def download_all_blobs_in_container(self):
        container_client = self.blob_service_client.get_container_client(self.container_name)
        blob_list = container_client.list_blobs()
        
        for blob in blob_list:
            downloaded_file_path = self.download_blob_to_file(blob.name)
            if downloaded_file_path:
                print(f"Downloaded to: {downloaded_file_path}")
            else:
                print(f"Skipped: {blob.name}")



class AzureBlobContainer:
    def __init__(self):
        load_dotenv()
        self.connection_string = self._get_connection_string()
        self.endpoint = os.getenv("AZURE_STORAGE_ENDPOINT")
        self.api_key = os.getenv("AZURE_STORAGE_API_KEY")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        self.blob_service_client = self.get_blob_service_client_account_key()

    def _get_connection_string(self):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string.startswith("DefaultEndpointsProtocol="):
            connection_string = "DefaultEndpointsProtocol=" + connection_string
        return connection_string

    def get_blob_service_client_account_key(self):
        account_url = self.endpoint
        credential = self.api_key
        return BlobServiceClient(account_url, credential=credential)

    def create_blob_container(self):
        try:
            self.blob_service_client.create_container(name=self.container_name)
        except ResourceExistsError:
            print('A container with this name already exists')

    def download_blob_to_file(self, blob_name):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
        file_name = blob_name.split("/")[-1]
        subfolder = blob_name.split("/")[-2]
        os.makedirs(os.path.join('blob_files', subfolder), exist_ok=True)
        file_path = os.path.join('blob_files', subfolder, file_name)

        if os.path.exists(file_path):
            print(f"File already exists: {file_path}")
            return None

        with open(file_path, mode="wb") as sample_blob:
            download_stream = blob_client.download_blob()
            sample_blob.write(download_stream.readall())

        return file_path

    def download_all_blobs_in_container(self):
        container_client = self.blob_service_client.get_container_client(self.container_name)
        blob_list = container_client.list_blobs()

        for blob in blob_list:
            downloaded_file_path = self.download_blob_to_file(blob.name)
            if downloaded_file_path:
                print(f"Downloaded to: {downloaded_file_path}")
            else:
                print(f"Skipped: {blob.name}")

    def list_blobs_flat(self):
        container_client = self.blob_service_client.get_container_client(container=self.container_name)
        blob_list = container_client.list_blobs(include=['tags', 'metadata'])

        for blob in blob_list:
            print(f"Name: {blob['name']}, Tags: {blob['tags']}, Metadata: {blob['metadata']}")

    def set_blob_metadata(self):
        container_client = self.blob_service_client.get_container_client(container=self.container_name)
        blob_list = container_client.list_blobs()

        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob)
            perimeter = blob_client.blob_name.split("/")[1]
            investigations_number = blob_client.blob_name.split("/")[2]
            year = investigations_number.split("-")[1]
            metadata = {'docType': 'pdf', 'perimeter': perimeter, 'investigations_number': investigations_number, 'year': year}
            blob_client.set_blob_metadata(metadata=metadata)

    def get_metadata_for_all_blobs(self):
        container_client = self.blob_service_client.get_container_client(container=self.container_name)
        blob_list = container_client.list_blobs()

        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob)
            blob_metadata = blob_client.get_blob_properties().metadata
            for k, v in blob_metadata.items():
                print(k, v)

    def set_properties_for_all_blobs(self):
        container_client = self.blob_service_client.get_container_client(container=self.container_name)
        blob_list = container_client.list_blobs()

        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob)
            blob_properties = blob_client.get_blob_properties()
            blob_headers = ContentSettings(content_type='application/pdf',
                                            content_language='fr',
                                            content_disposition='inline',
                                            cache_control='max-age=604800',
                                            content_encoding='utf-8')
            blob_client.set_http_headers(blob_headers)

    def get_properties_for_all_blobs(self):
        container_client = self.blob_service_client.get_container_client(container=self.container_name)
        blob_list = container_client.list_blobs()

        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob)
            blob_properties = blob_client.get_blob_properties()
            print(f"Blob type: {blob_properties.blob_type}")
            print(f"Blob size: {blob_properties.blob_size}")
            print(f"Content type: {blob_properties.content_settings.content_type}")
            print(f"Content encoding: {blob_properties.content_settings.content_encoding}")
            print(f"Content language: {blob_properties.content_settings.content_language}")
            print(f"Content disposition: {blob_properties.content_settings.content_disposition}")
            print(f"Content MD5: {blob_properties.content_settings.content_md5}")
            print(f"Blob name: {blob_properties.name}")