from pydantic import BaseModel
import uuid

###########################################################
### Модели для запросов ###
###########################################################

class RequestIDGet(BaseModel):
    id: uuid.UUID