from typing import Optional, Union
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class ModelName(str, Enum):
    alexnet = "alexnet2"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/test/{item_id2}/")
async def read_item(item_id2: str, q: str | None = None, short: bool = False):
    print(short)
    if q:
        return {"item_id": item_id2, "q": q}
    return {"item_id": item_id2}

@app.get("/items/{item_id}/user/{user_id}")
async def find_user_item(item_id: int, user_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
@app.get("/list")
def board_list():
    return [{1: "1번 게시글", 2: "2번 게시글"}]

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Hi, Nice to meet you"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "Hello ~ Good to see you"}

@app.get("/files/{file_path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

fake_item_db = [{"name": "juna", "age":29, "hobby":"study"}, {"name": "subin", "age": 29, "hobby": "reading book"}]
@app.get("/items/")
async def read_list(skip: int = 0, limit: int = 1):
    return fake_item_db[skip: skip + limit]

