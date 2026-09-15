import warnings
warnings.filterwarnings('ignore')

import os, sys,json
from typing import TypedDict, Optional

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

from bin.ai.tools.animal_checker import get_search
from bin.ai.tools.animal_datastructure import *
from bin.ai.tools.selected_animal_info import (
    animal_data_grabber,
    adw_page_reader,
    wikipedia_page_reader,
)

load_dotenv()


# ---------------------------------------------------------------------------
# One shared state schema for the whole graph, instead of a different
# ad-hoc class per node. Every node reads/writes a subset of these keys.
# ---------------------------------------------------------------------------
class PipelineState(TypedDict):
    seed: WikipediaPage              # the initial input (name/key you start with)
    gbif_data: Optional[AnimalInfoResult]     # filled by node1
    adw_data: Optional[str]                  # filled by node2a
    wiki_data: Optional[str]                 # filled by node2b
    merged: Optional[dict]        # filled by merge node
    output: Optional[AnimalInfoResult]        # filled by polish node (final result)


# ---------------------------------------------------------------------------
# Node 1: GBIF data gathering (runs in parallel with the ADW/Wikipedia branch)
# ---------------------------------------------------------------------------
def node1_gbif(state: PipelineState) -> PipelineState:
    """Build the initial AnimalInfoResult from GBIF data."""
    result = animal_data_grabber.invoke(input={"animal_page": state["seed"]})
    return {"gbif_data": result}


# ---------------------------------------------------------------------------
# Node 2a: ADW structured fields
# ---------------------------------------------------------------------------
def node2a_adw(state: PipelineState) -> PipelineState:
    """Fetch structured info from ADW, keyed by scientific name."""
    scientific_name = state["seed"]["scientific_name"]
    result = adw_page_reader.invoke(input={"scientific_name": scientific_name})
    return {"adw_data": result}


# ---------------------------------------------------------------------------
# Node 2b: Wikipedia content (runs in parallel with node2a — both only need
# `seed`, not each other's output, so there's no reason to serialize them)
# ---------------------------------------------------------------------------
def node2b_wikipedia(state: PipelineState) -> PipelineState:
    """Fetch supplementary content from Wikipedia, keyed by name/usageKey."""
    name = state["seed"]["key"]
    result = wikipedia_page_reader.invoke(input={"name": name})
    return {"wiki_data": result}


# ---------------------------------------------------------------------------
# Merge node: waits for node1, node2a, and node2b, then combines them.
# LangGraph automatically waits for every incoming edge before running this.
# ---------------------------------------------------------------------------
def merge_node(state: PipelineState) -> PipelineState:
    """Combine GBIF + ADW + Wikipedia data into a single working record."""
    gbif_data = (
        state["gbif_data"].model_dump()
        if state.get("gbif_data")
        else {}
    )

    merged = {
        "gbif": gbif_data,
        "adw": state.get("adw_data"),
        "wikipedia": state.get("wiki_data")[:30000],
    }

    return {"merged": merged}


# ---------------------------------------------------------------------------
# Polish node: rewrite/tighten the description using the merged data as
# source material (NOT verbatim copy — see licensing notes from earlier).
# ---------------------------------------------------------------------------
def polish_node(state: PipelineState) -> PipelineState:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3
    )

    structured_llm = llm.with_structured_output(AnimalInfoResult)

    merged = state["merged"]

    prompt = f"""
                You are creating a structured database record for an animal.

                Using the source information below, create a complete AnimalInfoResult.

                Rules:
                - Use the information from the sources.
                - Do not invent factual information.
                - Resolve conflicts between sources conservatively.
                - Prefer scientific sources when available.
                - Keep the generated description original.
                - Do not copy sentences verbatim from Wikipedia.
                - Fill every required field of AnimalInfoResult.

                SOURCE DATA:

                GBIF:
                {merged["gbif"]}

                ADW:
                {merged["adw"]}

                WIKIPEDIA:
                {merged["wikipedia"]}
                """

    final_result = structured_llm.invoke(prompt)

    return {"output": final_result}

# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------
builder = StateGraph(PipelineState)

builder.add_node("gbif", node1_gbif)
builder.add_node("adw", node2a_adw)
builder.add_node("wikipedia", node2b_wikipedia)
builder.add_node("merge", merge_node)
builder.add_node("polish", polish_node)

# Fan-out: all three data-gathering nodes start from START in parallel
builder.add_edge(START, "gbif")
builder.add_edge(START, "adw")
builder.add_edge(START, "wikipedia")

# Fan-in: merge waits for all three branches to finish
builder.add_edge("gbif", "merge")
builder.add_edge("adw", "merge")
builder.add_edge("wikipedia", "merge")

# Then polish, then end
builder.add_edge("merge", "polish")
builder.add_edge("polish", END)

graph = builder.compile()


def animal_data_creating(input:WikipediaPage):
    result = graph.invoke({"seed":input})
    return result

if __name__ == "__main__":
    
    seed_input = {
                    "id": 24408,
                    "key": "Polar_bear",
                    "title": "Polar bear",
                    "excerpt": None,
                    "matched_title": None,
                    "anchor": None,
                    "description": "Species of bear native to the Arctic",
                    "thumbnail": {
                        "mimetype": "image/jpeg",
                        "size": None,
                        "width": 60,
                        "height": 60,
                        "duration": None,
                        "url": "//thumb.wikimedia.org/wikipedia/commons/thumb/6/66/Polar_Bear_-_Alaska_%28cropped%29.jpg/60px-Polar_Bear_-_Alaska_%28cropped%29.jpg?utm_source=en.wikipedia.org&utm_campaign=rest&utm_content=thumbnail"
                    },
                    "scientific_name": "Ursus maritimus"
                }
    result = graph.invoke({"seed": seed_input})

    with open("file.json",'w') as f:
        json.dump(result['output'].model_dump(),f)
    print(result["output"])