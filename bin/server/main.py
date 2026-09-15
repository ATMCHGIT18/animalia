import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from bin.ai.tools.animal_checker import WikiSearchResult ,WikipediaPage
from bin.ai.tools.selected_animal_info import AnimalInfoResult
from bin.ai.agents.animal_cleaning_agent import animal_cleaning_query_agent
from bin.ai.agents.animal_info_agent import animal_data_creating

import uvicorn


app = FastAPI()

# 1. Enable CORS so your React app (usually running on port 5173 or 3000) can talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    query: str

@app.post("/api/search-animals", response_model=WikiSearchResult)
def search_animals(payload: SearchRequest):
    try:
        if not payload.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
            
        result = animal_cleaning_query_agent(message=payload.query)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class SelectedAnimalRequest(BaseModel):
    selectedAnimal: WikipediaPage

@app.post("/api/create_selected_animal",response_model=AnimalInfoResult)
def create_animal_info(payload:SelectedAnimalRequest):
    try:
        
        if not payload.title.strip():
            raise HTTPException(status_code=400,detail="Query cannot be empty please check it")

        result = animal_data_creating(message=payload.selectedAnimal)
        return result
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)