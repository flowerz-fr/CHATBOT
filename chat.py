import json
from collections import OrderedDict
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
import os
from langchain_community.retrievers import AzureAISearchRetriever


class Chatbot:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2023-05-15",
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            model="gpt-35-turbo",
            temperature=0,
        )

        self.index_name = "complete_dataset"
        self.retriever = AzureAISearchRetriever(
            content_key="content", top_k=30, index_name=self.index_name
        )

        system_prompt = (
            "Use the given context to answer the question. "
            "If you don't know the answer, say you don't know. "
            "Use five sentences maximum and keep the answer concise. "
            "Context: {context}"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        self.question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        self.chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    def ask(self, user_query):
        result = self.chain.invoke({"input": user_query})
        
        def extract_list_sources(result):
                sources = []
                for doc in result['context']:
                    try:
                        data = doc.metadata['metadata']
                        data = json.loads(data)
                        source = data.get('Source')
                        if source:
                            sources.append(source)
                    except json.JSONDecodeError:
                        # Handle the case where metadata is not a valid JSON
                        continue
                sources = list(OrderedDict.fromkeys(sources))  # Remove duplicates while preserving order
                return sources
        
        # Create the json_result
        json_result = {
            "input": result['input'],
            "sources": extract_list_sources(result),
            "answer": result['answer']
        }
    
        return json_result