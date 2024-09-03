import os
from abc import ABC, abstractmethod
from base_app.consonants import SourceTypes, SpaceTopics

class BaseSourceResponse(ABC):
    
    def __init__(self):
        os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
        os.environ['LANGCHAIN_API_KEY']=os.getenv("LANGCHAIN_API_KEY")
        os.environ['LANGCHAIN_TRACING_V2']=os.getenv("LANGCHAIN_TRACING_V2")
        os.environ['LANGCHAIN_PROJECT']=os.getenv("LANGCHAIN_PROJECT")
        os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")

    
    def get_topic_label(self, topic_slug : str) -> str:
        label = SpaceTopics.get_space_topic_label_by_topic_slug(topic_slug)
        return label
    
    @abstractmethod
    def get_response(self, query):
        pass