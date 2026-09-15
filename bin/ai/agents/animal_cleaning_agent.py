import warnings
warnings.filterwarnings('ignore')

import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)


from langchain_openai import ChatOpenAI
from langgraph.prebuilt import tools_condition
from langgraph.graph import END
from dotenv import load_dotenv
from bin.ai.tools.animal_checker import get_search
from bin.ai.tools.animal_datastructure import WikiSearchResult 

load_dotenv()


# Animal Search Result Checker from Wikipedia Source

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
        f"In the end complete the missing data inside the json for each point specially the scientific_name sections is really important to be found and put"
    )
    
    return structured_shaper.invoke(shaper_prompt)
