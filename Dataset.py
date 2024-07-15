import os
import pandas as pd
from Document import Document

class DatasetBuilder:
    def __init__(self, start_directory):
        self.start_directory = start_directory
        self.data = []

    @staticmethod
    def extract_metadata_and_content(document):
        metadata = document.get('metadata', {})
        page_content = document.get('page_content', '')
        return metadata, page_content

    def process_document(self, file_path):
        # Replace PDFDocumentProcessor with actual document processing implementation
        processor = Document(file_path)
        document = processor.process_document()
        metadata, page_content = self.extract_metadata_and_content(document)
        row = {
            'Title': metadata.get('Title'),
            'Version': metadata.get('Version'),
            'Date': metadata.get('Date'),
            'Confidentiality': metadata.get('Confidentiality'),
            'Perimeter': metadata.get('Perimeter'),
            'Investigation Number': metadata.get('Investigation Number'),
            'page_content': page_content,
            'Source': metadata.get('Source')
        }
        self.data.append(row)

    def process_directory(self):
        for root, dirs, files in os.walk(self.start_directory):
            for file in files:
                if file.endswith('.pdf'):  # Adjust the file extension as needed
                    file_path = os.path.join(root, file)
                    self.process_document(file_path)
        return pd.DataFrame(self.data)
    