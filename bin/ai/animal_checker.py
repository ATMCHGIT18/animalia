import warnings
warnings.filterwarnings('ignore')

from wiki_tools import wiki_page
from langchain_openai import ChatOpenAI,OpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
from typing import List

load_dotenv()

@tool("wikipedia-animal-check")
def get_search(query:str) -> dict:
    '''This is the tool that when ever a word is typed then this will be executed to 
    see that if the results that came from the wikipedia rest api is infact an animal or not.
    So this tool is actually is being used to filter the result of the output of the 
    rest api which it is pages
    
    pages is a json file that contains these things. But you as an agent need to see only
    title of each page and if the page refered to an animal then keep it and if it does not
    about to an animal then delete that object.'''

    pages = wiki_page(search_query=query,number_of_results=5)
    return pages

