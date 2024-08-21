from document_processor import DocumentProcessor
import pandas as pd
import os

class DirectoryProcessor:
    def __init__(self, start_directory):
        self.start_directory = start_directory
        self.data = []

    def process_document(self, file_path):
        """Process a single document and append its data to the internal list."""
        processor = DocumentProcessor(file_path)
        document = processor.process_document()
        metadata = document.get('metadata', {})
        page_content = document.get('page_content', '')

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
        """Process all PDF documents in the directory and return a DataFrame."""
        for root, dirs, files in os.walk(self.start_directory):
            for file in files:
                if file.endswith('.pdf'):
                    file_path = os.path.join(root, file)
                    self.process_document(file_path)
        return pd.DataFrame(self.data)

# Example:

# # To process all PDFs in a directory
# directory_processor = DirectoryProcessor('path/to/the/directory')
# dataset = directory_processor.process_directory()
