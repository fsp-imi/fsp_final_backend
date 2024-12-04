from typing import Annotated
from fastapi import FastAPI, Query, Body
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float 
    tax: float | None = None

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello world!'}

@app.get('/items/{item_id}/')
def items(item_id: int):
    return {'item_id':item_id}

@app.get('/items/')
def itemspages(q: Annotated[list[str] | None, Query(max_length=150)] = None):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update(q)
    return result

@app.post('/items/')
async def create(item: Item):
    #create object
    return item



