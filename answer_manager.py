import json
from collections import OrderedDict

class ResultProcessor:
    def __init__(self, max_sources=4):
        """
        Initializes the ResultProcessor with an optional maximum number of sources to include.

        :param max_sources: The maximum number of unique sources to include in the result. Default is 4.
        """
        self.max_sources = max_sources

    def extract_list_sources(self, result):
        """
        Extracts a list of unique sources from the result's context metadata.

        :param result: A dictionary containing the result with a 'context' key.
        :return: A list of unique sources, limited by the max_sources attribute.
        """
        sources = []
        for doc in result.get('context', []):
            try:
                # Extract the metadata and parse it as JSON
                metadata = doc.metadata.get('metadata', '{}')
                metadata_dict = json.loads(metadata)
            
                # Get the source from the parsed metadata
                source = metadata_dict.get('Source')
                if source:
                    sources.append(source)
                    
            except json.JSONDecodeError:
                # Handle cases where the metadata is not valid JSON
                continue
            except AttributeError:
                # Handle cases where 'metadata' or 'Source' might not exist
                continue

        # Remove duplicates while preserving the order
        unique_sources = list(OrderedDict.fromkeys(sources))

        # Return the limited number of sources
        return unique_sources[:self.max_sources]

    def create_json_result(self, result):
        """
        Creates a JSON-like result with input, sources, and answer.

        :param result: A dictionary containing the result with 'context', 'input', and 'answer' keys.
        :return: A dictionary with 'input', 'sources', and 'answer'.
        :raises KeyError: If 'input' or 'answer' keys are missing in the result.
        """
        try:
            json_result = {
                "input": result['input'],
                "sources": self.extract_list_sources(result),
                "answer": result['answer']
            }
            return json_result
        except KeyError as e:
            raise KeyError(f"Missing expected key in the result: {str(e)}")





