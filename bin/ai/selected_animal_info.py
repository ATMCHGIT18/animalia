import warnings
warnings.filterwarnings('ignore')

import os,sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import List
import json
from pydantic import BaseModel,Field


class AnimalInfoResult(BaseModel):
    status:str = Field(description="Status of the animal. ")