import warnings
warnings.filterwarnings('ignore')

import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)


from bin.ai.wiki_tools import wiki_page
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.prebuilt import tools_condition
from langgraph.graph import END
from dotenv import load_dotenv
from typing import List
import json
from pydantic import BaseModel,Field

load_dotenv()

TOOL_CALL_COUNTS = 0

class WikipediaThumbnailPage(BaseModel):
    mimetype:str = Field(description="Thumbnail media type")
    size:int | None = Field(description="File size in bytes or null if not available",default=None)
    width:int | None = Field(description=" Maximum recommended image width in pixels or null if not available",default=None)
    height:int | None = Field(description="Maximum recommended image height in pixels or null if not available",default=None)
    duration:int | None = Field(description="Length of the video, audio, or multimedia file or null for other media types",default=None)
    url:str = Field(description="URL to download the file")

class WikipediaPage(BaseModel):
    id:int = Field(description="Page identifier which is integer number")
    key:str =Field(description="Page title in URL-friendly format")
    title:str = Field(description="The exact title of the wikipedia page")
    excerpt:str | None = Field(default=None,description="A few lines giving a sample of page content with search terms highlighted with <span class=\"searchmatch\"> tags. Excerpts may end mid-sentence")
    matched_title:str | None = Field(default=None,description="Title of the page redirected from, if the search term originally matched a redirect page or null if search term did not match a redirect page")
    anchor:str | None = Field(description="Just put the anchor there if it is inside this key unless it is null",default=None)
    description:str | None = Field(description="Short summary of the page topic based on the corresponding entry on Wikidata or null if no entry exists.",default=None)
    thumbnail:WikipediaThumbnailPage | None = Field(description="Reduced-size version of the page's lead image or null if no lead imagine exists",default=None)

class WikiSearchResult(BaseModel):
    query:str = Field(description="The original search result")
    results: List[WikipediaPage] = Field(description="A list of  matching Wikipedia pages")


@tool("wikipedia-animal-check",response_format='content')
def get_search(query:str) -> WikiSearchResult:
    '''Search Wikipedia and retrieve raw pages matching the query text only and only once. 
    Use this tool to gather potential candidate pages.
    and then do what ever you need to do them with'''

    global TOOL_CALL_COUNTS
    TOOL_CALL_COUNTS += 1

    if TOOL_CALL_COUNTS > 3 :
        return WikiSearchResult(query=str(query), results=[])

    if isinstance(query, dict):
        query = query.get("query", str(query))
    elif str(query).startswith("{") and "query" in str(query):
        try:
            query = json.loads(query).get("query", query)
        except Exception:
            pass

    pages = wiki_page(search_query=query,number_of_results=10)

    formatted_pages = []

    for page in pages:
        if (page['thumbnail'] == None):
            thumbnail = None
        else:
            thumbnail = WikipediaThumbnailPage(
                mimetype=page['thumbnail'].get('mimetype'),
                size = page['thumbnail'].get('size',None),
                width= page['thumbnail'].get('width',None),
                height= page['thumbnail'].get('height',None),
                duration= page['thumbnail'].get('duration',None),
                url= page['thumbnail'].get('url')
            )

        item = WikipediaPage(
            id= page.get("id"),
            key=page.get('key'),
            title=page.get('title'),
            matched_title=page.get('matched_title',None),
            anchor=page.get('anchor',None),
            description=page.get('description'),
            thumbnail=thumbnail
        )

        formatted_pages.append(item)

    return WikiSearchResult(query=query,results=formatted_pages)

def strict_one_call_router(state) -> str:
    messages = state["messages"]
    tool_calls_count = 0
    
    for msg in messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tool_calls_count += 1
            
    if tool_calls_count >= 1:
        return END
        
    return tools_condition(state)



def animal_cleaning_query_agent(message: str) -> WikiSearchResult:
    '''Animal Search Cleaning Agent'''
    gpt = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    
    raw_search_data = get_search.invoke({"query": message})
    
    structured_shaper = gpt.with_structured_output(WikiSearchResult)
    
    shaper_prompt = (
        f"You are a strict data-cleaning assistant specializing in zoology and biological science.\n"
        f"Analyze the following pre-fetched Wikipedia dataset:\n\n{raw_search_data.model_dump_json()}\n\n"
        f"Your task is to filter out any results that are NOT living or historical biological animals.\n\n"
        f"CRITICAL FILTERING CRITERIA:\n"
        f"1. KEEP only real, biological animal species, subspecies, or direct animal groups (e.g., Panthera leo, Mammals, Birds).\n"
        f"2. EXCLUDE anything that is an artificial object, artwork, sculpture, monument, or human artifact (e.g., 'Lion-man sculpture', 'Sphinx').\n"
        f"3. EXCLUDE mythological creatures, fictional characters, movies, sports teams, or pop-culture references (e.g., 'The Lion King', 'Detroit Lions').\n"
        f"4. Look deeply at the 'description' and 'title'. If the description mentions words like 'sculpture', 'statue', 'film', 'character', 'book', or 'artifact', you MUST filter it out.\n\n"
        f"EXECUTION INSTRUCTION:\n"
        f"For each item, silently ask yourself: 'Is this an actual biological animal?' If the answer is no, delete it.\n\n"
        f"Return only the remaining true animal items matching the WikiSearchResult schema perfectly. Set the final 'query' field to: '{message}'."
    )
    
    return structured_shaper.invoke(shaper_prompt)

#  Running example ----------------------------------------------------------------------

# if __name__ == "__main__":
#     query = input("Please search an animal (or type 'exit'): \n")
#     while query != "exit":
#         try:
#             result = animal_cleaning_query_agent(message=query)
#             print("\n✨ Output Pydantic Instance Content:")
#             print(f"Query: {result.query}")
#             print(f"Results Count: {len(result.results)}")
#             for idx, item in enumerate(result.results):
#                 print(idx , item)
#         except Exception as e:
#             print(f"🛑 Error handling execution: {e}")
            
#         print("\n" + "="*40 + "\n")
#         query = input("Please search an animal (or type 'exit'): \n")


