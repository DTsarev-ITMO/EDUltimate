from pydantic import BaseModel
import uuid

class RequestGetID(BaseModel):
    id: uuid.UUID