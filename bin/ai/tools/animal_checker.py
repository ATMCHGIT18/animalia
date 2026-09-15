import warnings
warnings.filterwarnings('ignore')

import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)


from bin.ai.tools.wiki_tools import wiki_page
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import tools_condition
from langgraph.graph import END
from dotenv import load_dotenv
import json

from bin.ai.tools.animal_datastructure import WikiSearchResult , WikipediaThumbnailPage ,  WikipediaPage

TOOL_CALL_COUNTS = 0

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
            scientific_name=None,
            key=page.get('key'),
            title=page.get('title'),
            matched_title=page.get('matched_title',None),
            anchor=page.get('anchor',None),
            description=page.get('description'),
            thumbnail=thumbnail
        )

        formatted_pages.append(item)

    return WikiSearchResult(query=query,results=formatted_pages)





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


