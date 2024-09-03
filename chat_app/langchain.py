import os
from base_app.langchain import BaseSourceResponse
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_community.vectorstores import FAISS


class LargeLanguageModelSourceResponse(BaseSourceResponse):

    def __init__(self, query:str, topic:str, model:str, user:str, **kwargs):
        self.query = query
        self.topic = topic
        self.model = model
        self.user = user
        self.groq_api_key=os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(model=self.model, groq_api_key=self.groq_api_key)
        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a helpful assistant for answering questions about '{topic}' topic only.
            Please provide the most accurate response based on the question.
            if you do not know the answer, please say "I do not know".
            if user asked unrelated topic question then explain to user that currently you can discuss with current topic only.
            Question:{query}
            """
        )
        self.chain = self.prompt|self.llm|StrOutputParser()
        
    def get_response(self):
        response = self.chain.stream({
            "topic" : self.get_topic_label(self.topic),
            "query" : self.query or "Hi!"
        })
        return response



class PretrainedPdfFileSourceResponse(BaseSourceResponse):
    

    def get_response(self, query):
        pass
        
        

