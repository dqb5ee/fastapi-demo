#!/Users/avalonbennett/.local/share/virtualenvs/fastapi-demo-M6wBm4_e/bin/python3

from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import json
import os


app = FastAPI()

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Avalon"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("customer/{idx}")
def customer(idx: int):
    df = pd.read_csv("customers.csv")
    customer = df.iloc[idx]
    return customer.to_dict()

@app.post("/get_body")
async def get_body(request: Request):
    response = await request.json()
    first_name = response["fname"]
    last_name = response["lname"]
    return {"first_name": first_name, "last_name": last_name}
    ####### return await request.json()

