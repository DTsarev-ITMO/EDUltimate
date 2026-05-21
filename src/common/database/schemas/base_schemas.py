from pydantic import BaseModel
import uuid

class ResponseGetID(BaseModel):
    id: uuid.UUID