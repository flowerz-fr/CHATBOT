import pandas as pd
from langchain_community.document_loaders import DataFrameLoader

class DocumentLoaderManager:
    def __init__(self, data: pd.DataFrame, page_content_column: str = "page_content"):
        """
        Initializes the DocumentLoaderManager with a DataFrame and the specified content column.

        :param data: A pandas DataFrame containing the data to be processed.
        :param page_content_column: The column name containing the text content to be loaded.
        """
        self.data = data
        self.page_content_column = page_content_column

    def load_documents_from_dataframe(self):
        """
        Loads documents from the DataFrame using DataFrameLoader.

        :return: A list of documents loaded from the DataFrame.
        :raises ValueError: If the DataFrame is empty or the specified column is not found.
        :raises RuntimeError: If there is an error during the document loading process.
        """
        if self.data.empty:
            raise ValueError("The DataFrame is empty.")
        
        if self.page_content_column not in self.data.columns:
            raise ValueError(f"Column '{self.page_content_column}' not found in DataFrame.")
        
        try:
            loader = DataFrameLoader(self.data, page_content_column=self.page_content_column)
            documents = loader.load()
            print("Documents loaded successfully.")
            return documents
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading documents: {str(e)}")
        