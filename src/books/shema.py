from pydantic import BaseModel
from typing import List, Optional


class CreateBook(BaseModel):
    
    titel: str
    author_ids: Optional[List[int]] = None
