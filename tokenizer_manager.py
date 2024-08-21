import tiktoken

class DocumentTokenizer:
    def __init__(self):
        """
        Initializes the DocumentTokenizer with a specified encoding.
        
        :param encoding: The encoding to use for tokenization.
        """
        # Initialize tokenizer with the specified encoding
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def tokenize(self, text):
        """
        Tokenizes text and returns the number of tokens.

        :param text: The text to be tokenized.
        :return: The number of tokens in the text.
        """
        tokens = self.tokenizer.encode(text, disallowed_special=())
        return tokens

    def token_count(self, text):
        """
        Returns the number of tokens in the text.

        :param text: The text to be tokenized.
        :return: The number of tokens in the text.
        """
        return len(self.tokenize(text))
