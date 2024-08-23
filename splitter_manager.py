from langchain_text_splitters import RecursiveCharacterTextSplitter
from tokenizer_manager import DocumentTokenizer

class DocumentSplitter:
    def __init__(self):
        """
        Initializes the DocumentSplitter with specified parameters.
        """
        tokenizer = DocumentTokenizer() #   param tokenizer: An instance of DocumentTokenizer to calculate token lengths.
        separators=None #   param separators: A list of separators used for splitting the document.
        chunk_size=100  #   param chunk_size: The size of each chunk after splitting the document.
        chunk_overlap=5 #   param chunk_overlap: The overlap between chunks to maintain context.
        
        if separators is None:
            separators = ["\n", " ", ""]
        
        # Initialize text splitter with given parameters
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=tokenizer.token_count,
            separators=separators
        )

    def split_documents(self, documents):
        """
        Splits the provided documents into smaller chunks.

        :param documents: A list of documents to be split.
        :return: A list of split document chunks.
        """
        try:
            splits = self.text_splitter.split_documents(documents)
            print("Documents split successfully.")
            return splits
        except Exception as e:
            raise RuntimeError(f"An error occurred while splitting documents: {str(e)}")
