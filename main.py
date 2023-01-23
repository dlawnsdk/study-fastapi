from typing import Optional
from enum import Enum
from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Required

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

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

class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items2/")
async def create_item(item: Item2):
    item_dict = item.dict() # dictionary Type으로 변환
    if item.tax:
        price_width_tax = item.price + item.tax
        item_dict.update({"price_width_tax": price_width_tax})
    return item_dict

@app.put("/items2/{item_id}")
async def create_item(item_id: int, item: Item2):
    item.name = "imjuna"
    return {"item_id": item_id, **item.dict()}

@app.put("/items3/{item_id}")
async def create_item(item_id: int, item: Item2, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

@app.get("/items3/")
async  def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return  results

@app.get("/items4/")
async def read_items(q: str | None  = Query(default=None, min_length=10 ,max_length=50, regex="(http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q":q})
    return results

@app.get("/items5/")
async def read_items(q: str = Query(default="Default Data Allowed", min_length=3)):
    results = {"items": [{"item_id": "001"}, {"item_id": "002"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/item6/")
async def read_items(q: str = Query(default=..., min_length=3)): # default=Required
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/items7/")
async def read_items(q: list[str] | None = Query(default=None, title="Query String", description="Testing", alias="Item Alias")):
    query_items = {"q" : q}
    return query_items

@app.get("/items8/{item_id}")
async def read_items(item_id: int = Path(title = "The Id of the item to get"), q: str | None = Query(default=Required, alias="Item-query")):
    results = {"item_id": item_id}
    if q:
        results.update({"q":q})
    return results

# gt: 크거나(greater than)
# ge: 크거나 같은(greater than or equal)
# lt: 작거나(less than)
# le: 작거나 같은(less than or equal)
@app.get("/items9/{item_id}")
async def read_times(*, item_id: int = Path(title = "Id title~", gt=10, le=100), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.put("/items10/{item_id}")
async def update_item(*, item_id: int = Path(title="The Id of the item to get", ge=0, le=1000), q:str | None = None, item: Item2 | None = None,):
    results = {"item_id": item_id}
    item.name = "imjuna"
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

class User(BaseModel):
    username: str
    full_name: str | None = None
@app.put("/item11/{item_id}")
async def update_item(item_id: int, item:Item, user:User):
    results = {"item_id": item_id, "item":item, "user": user}
    return results

@app.put("/items12/{item_id}")
async def update_item(item_id:int, item:Item2, user:User, importance:int = Body()):
    importance = 5
    results = {"item_id": item_id, "item": item, "user":user, "importance": importance}
    return results