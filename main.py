from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import json
import pandas as pd
from pandasql import sqldf
from sqlalchemy import create_engine
from fastapi import FastAPI, File, Form, UploadFile
import shutil
import sqlite3
import ast
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
engine = create_engine(
    "mysql+pymysql://{user}:{pw}@localhost/{db}".format(
        user="root", pw="root",  db="exams"
    )
)

def convertUploadedFileJson(fileName):
    with open(f"{fileName}", "r") as f:
        data = json.loads(f.read())
    ques = pd.io.json.json_normalize(data)
    ques["material"] = str(fileName.replace(".json", ""))
    out = ques.reset_index().to_json(orient="records")
    dfJson = json.loads(out)
    return dfJson

def insertIntoDB():
    rows = []
    for field in data:
        query="""
            INSERT IGNORE INTO exams (  numb, question, answer,options,material)
            VALUES ( '{}','{}','{}',"{}","{}");""".format( field["numb"],field["question"],field["answer"],field["options"],field['material'])
        print("Inserting {},{}".format(field['numb'],field["material"]))
        try:
            engine.execute(query)
        except Exception as e:
            print(f"Error {e}")


def convertIt(fileName, count):
    with open(f"{fileName}", "r") as f:
        data = json.loads(f.read())
    ques = pd.io.json.json_normalize(data)
    ques.to_csv("output.csv")
    data = pd.read_csv("output.csv", usecols=["numb", "question", "answer", "options"])
    output = sqldf(
        "select * from data where numb  >= (abs(random()) % (SELECT max(numb) FROM data)) limit {}".format(
            count
        )
    )
    out = output.reset_index().to_json(orient="records")
    dfJson = json.loads(out)
    return data, output, dfJson


def convertItandInsert(fileName):
    with open(f"{fileName}", "r") as f:
        data = json.loads(f.read())
    ques = pd.io.json.json_normalize(data)
    ques.to_csv("output.csv")
    data = pd.read_csv("output.csv", usecols=["numb", "question", "answer", "options"])
    output = sqldf(
        "select * from data where numb  >= (abs(random()) % (SELECT max(numb) FROM data)) limit {}".format(
            count
        )
    )
    out = output.reset_index().to_json(orient="records")
    dfJson = json.loads(out)
    return data, output, dfJson


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Name": "Exams API"}


# analysis
@app.get("/items/{item_id}")
def read_item(item_id: str, count: Optional[int] = None):
    # conn = sqlite3.connect("save_exams.db")
    # df = pd.read_sql_query(f"select * from {item_id} limit {count};", conn)
    df = pd.read_sql(f"select * from exams where material = '{item_id}' limit {count};", con=engine)

    out = df.reset_index().to_json(orient="records")
    dfJson = json.loads(out)
    return dfJson


@app.put("/items/{item_id}")
def update_item(
    item: str,
    index: int,
    numb: int,
    question: str,
    options1: str,
    options2: str,
    options3: str,
    options4: str,
    answer: str,
):
    obj = {
        "item": item,
        "index": index,
        "numb": numb,
        "question": question,
        "options": [options1, options2, options3, options4],
        "answer": answer,
    }
    op = [options1, options2, options3, options4]
    conn = sqlite3.connect("save_exams.db")
    c = conn.cursor()
    print(
        f"""insert into {item} values("{index}","{numb}","{question}","{answer}","{op}")"""
    )
    c.execute(
        f"""insert into {item} values("{index}","{numb}","{question}","{answer}","{op}")"""
    )
    conn.commit()
    return obj


@app.post("/files/")
async def create_file(
    file: UploadFile = File(...),
):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    convertItandInsert(file.filename)
    return {"file_size": file.filename}
