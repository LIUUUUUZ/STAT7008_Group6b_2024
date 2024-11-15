import openai
from langchain_openai import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

class ChatBot():
    def __init__(self, api_key: str = "", init_prompt: str = ""):
        openai.api_key = api_key
        self.chat = ChatOpenAI(openai_api_base="https://chatapi.littlewheat.com/v1", openai_api_key=openai.api_key)
        self.init_prompt: str = init_prompt
        self.messages = [SystemMessage(content = self.init_prompt)]

    def send_message(self, human_input: str) -> str:
        self.messages.append(HumanMessage(content=human_input))
        response = self.chat(self.messages)
        self.messages.append(AIMessage(content = response.content))
        while len(self.messages) > 20:
            self.messages.pop(0)
        return response.content

    def __call__(self, human_input: str) -> str:
        return self.send_message(human_input)
    
    def set_api_key(self, api_key: str):
        openai.api_key = api_key
        self.chat = ChatOpenAI(openai_api_base="https://chatapi.littlewheat.com/v1", openai_api_key=openai.api_key)

    
    def __str__(self) -> str:
        return "STAT7008_Group6b_Chatbot"