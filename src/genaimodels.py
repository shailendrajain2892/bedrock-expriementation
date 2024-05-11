from typing import Union

from fastapi import FastAPI
import boto3

app = FastAPI()
brclient = boto3.client('bedrock')

@app.get("/get_foundation_models")
def get_foundation_models():
    models  = brclient.list_foundation_models()
    return [model.get('modelId') for model in models.get('modelSummaries')]

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}