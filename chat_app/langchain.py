import os
from operator import itemgetter
from base_app.langchain import BaseSourceResponse
from base_app.consumers import BaseChatBotAsyncJsonWebsocketConsumer
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, trim_messages
from langchain_community.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper,ArxivAPIWrapper
from langchain.agents import initialize_agent,AgentType

class LargeLanguageModelSourceResponse(BaseSourceResponse):

    def __init__(self, query:str, topic:str, model:str, user:str, **kwargs):
        self.query = query
        self.topic = topic
        self.model = model
        self.user = user
        self.groq_api_key=os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(model=self.model, groq_api_key=self.groq_api_key)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    """
                    Your name is Bujji. You are a helpful assistant for answering questions about '{topic}' topic only.
                    Please provide the most accurate response based on the question.
                    if you do not know the answer, please say "I do not know".
                    if user asked unrelated topic question then explain to user that currently you can discuss with current topic only.
                    currently you are using {model} llm model.
                    """                 
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        
        self.chain = RunnablePassthrough.assign(messages=itemgetter("messages")|self.get_trimmer(self.llm))|self.prompt|self.llm|StrOutputParser()
        
        
    def get_trimmer(self, model):
        return trim_messages(
            max_tokens=1000,
            strategy="last",
            token_counter=model,
            include_system=True,
            allow_partial=False,
            start_on="human"
        )
        
    def get_messages(self, session_id):
        return BaseChatBotAsyncJsonWebsocketConsumer.get_session_messages(session_id)
        
    def get_response(self):
        
        config={"configurable":{"session_id":self.user}, "topic" : self.get_topic_label(self.topic)}
        human_message = HumanMessage(content=self.query or "Hi!")
        
        response = self.chain.stream({
            "messages" : self.get_messages(self.user) + [human_message], 
            "topic" : self.get_topic_label(self.topic),
            "model" : self.model,
        })
        return response

class WebSourceResponse(BaseSourceResponse):
    
    def __init__(self, query:str, topic:str, choice:str, user:str, **kwargs):
        self.query = query
        self.topic = topic
        self.choice = choice
        self.user = user
        self.tools = {}
        self.llm = ChatGroq(model="gemma2-9b-it", groq_api_key=os.getenv("GROQ_API_KEY"), streaming = True)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system", 
                    """
                    Your name is Bujji. You are a helpful assistant for answering questions about '{topic}' topic only.
                    Answer the question using the context below when the question is related to the topic.
                    if you do not know the answer, please say "I do not know".
                    currently you are using {choice} source.
                    
                    Context: {context}
                    """                 
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        
        self.chain = RunnablePassthrough.assign(messages=itemgetter("messages")|self.get_trimmer(self.llm))|self.prompt|self.llm|StrOutputParser()
        
        self.api_wrapper_wiki=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=5000)
        self.tools['wikipedia']=WikipediaQueryRun(api_wrapper=self.api_wrapper_wiki)
        self.api_wrapper_arxiv=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=5000)
        self.tools['arxiv']=ArxivQueryRun(api_wrapper=self.api_wrapper_arxiv)
        self.tools['duckduckgo']=DuckDuckGoSearchRun(name="Duck Duck Go Search")
    
        
    
    def get_messages(self, session_id):
        return BaseChatBotAsyncJsonWebsocketConsumer.get_session_messages(session_id)
    
    def get_trimmer(self, model):
        return trim_messages(
            max_tokens=1000,
            strategy="last",
            token_counter=model,
            include_system=True,
            allow_partial=False,
            start_on="human"
        )
    
    def get_response(self):
        context = self.tools[self.choice].run((self.query)) or ''
        config={"configurable":{"session_id":self.user}, "topic" : self.get_topic_label(self.topic)}
        human_message = HumanMessage(content=self.query or "Hi!")
        
        response = self.chain.stream({
            "messages" : self.get_messages(self.user) + [human_message], 
            "topic" : self.get_topic_label(self.topic),
            "choice" : self.choice,
            "context" : context,
        })        
        return response


class PretrainedPdfFileSourceResponse(BaseSourceResponse):
    
    def __init__(self, query:str, topic:str, user:str, **kwargs):
        self.query = query
        self.topic = topic
        self.user = user
     
    def get_response(self):
        for word in "Pretrained Pdf File Source Response Not Implemented Yet":
            yield word
        
        

