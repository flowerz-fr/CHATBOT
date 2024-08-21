# from collections import OrderedDict
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from prompt_manager import PromptManager
from llm_models import AzureOpenAIManager
from retriever_manager import ManagerRetrieve
from answer_manager import ResultProcessor

class QuestionAnswerManager:
    def __init__(self):
        self.llm = AzureOpenAIManager().create_chat()
        self.retriever = ManagerRetrieve().get_retriever()
        self.prompt = PromptManager().get_prompt()
        
        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    def ask(self, user_query):
        result = self.chain.invoke({"input": user_query})
        result =ResultProcessor().create_json_result(result)
        return result
        
