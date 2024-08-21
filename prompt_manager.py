from langchain_core.prompts import ChatPromptTemplate

class PromptManager:
    def __init__(self):
        """
        Initializes the PromptManager with a system prompt and a ChatPromptTemplate.
        """
        # Define the system prompt template
        self.system_prompt = (
            "Use the given context to answer the question. "
            "If you don't know the answer, say you don't know. "
            "Use five sentences maximum and keep the answer concise. "
            "Context: {context}"
        )

        # Initialize the ChatPromptTemplate with system and human prompts
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("human", "{input}"),
            ]
        )

    def get_prompt(self):
        """
        Returns the ChatPromptTemplate instance.

        :return: ChatPromptTemplate instance.
        """
        return self.prompt

    def get_system_prompt(self):
        """
        Returns the system prompt template.

        :return: System prompt string.
        """
        return self.system_prompt
