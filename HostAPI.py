from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

# Define a model for expected JSON
class Item(BaseModel):
    name: str
    quantity: int
    price: float

@app.post("/items")
async def create_item(item: Item):
    # Access parsed JSON as a Python object
    return {
        "message": "Item received successfully!",
        "data": item.dict()
    }
