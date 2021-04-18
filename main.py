from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import json
import pandas as pd
from pandasql import sqldf
from sqlalchemy import create_engine
from fastapi import FastAPI, File, Form, UploadFile
import shutil
from fastapi.middleware.cors import CORSMiddleware
import datetime
import os
from sdconfig import *
import uvicorn
import ast

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
    "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
        user=databaseUser, pw=databasePassword, db=databaseName, host=databaseHost
    )
)

try:
    engine.execute(createTable)
except Exception as e:
    print(e)
    exit(0)

def convertUploadedFileJson(fileName, fineOrigin):
    with open(f"{fileName}", "r") as f:
        data = json.loads(f.read())
    ques = pd.io.json.json_normalize(data)
    ques["material"] = str(fineOrigin.replace(".json", ""))
    out = ques.reset_index().to_json(orient="records")
    dfJson = json.loads(out)
    return dfJson


def getTimeStap():
    ts = datetime.datetime.now().timestamp()
    return ts


def insertIntoDB(dfjson):
    count = 0
    for field in dfjson:
        query = """
            INSERT IGNORE INTO exams (  numb, question, answer,options,material)
            VALUES ( '{}','{}','{}',"{}","{}");""".format(
            field["numb"],
            field["question"],
            field["answer"],
            field["options"],
            field["material"],
        )
        print("Inserting {},{}".format(field["numb"], field["material"]))
        try:
            engine.execute(query)
            count = count + 1
        except Exception as e:
            print(f"Error {e}")
    return count


@app.get("/")
def read_root():
    return {"Home": "Welcome to Exams API, check /docs for more info"}


# Get info [Done]
@app.get("/items/{item_id}")
def read_item(item_id: str, count: Optional[int] = None):
    df = pd.read_sql(
        f"select * from exams where material = '{item_id}' ORDER BY RAND() limit {count};",
        con=engine,
    )
    out = df.reset_index().to_json(orient="records")
    dfJson = json.loads(out)
    for index,val in enumerate(dfJson):
        try:
            x=dfJson[index]['options']
            dfJson[index]['options']=ast.literal_eval(x)
        except Exception as e:
            pass
    return dfJson


# Put questions [Done]
@app.put("/items/{item_id}")
def update_item(
    question: str,
    options1: str,
    options2: str,
    options3: str,
    options4: str,
    answer: str,
    material: str,
):
    obj = {
        "question": question,
        "options": [options1, options2, options3, options4],
        "answer": answer,
        "material": material,
    }
    op = [options1, options2, options3, options4]
    print(f"Trying to insert exams into material {material}")
    query = f"""insert into exams (question,options,answer,material) values("{question}","{op}","{answer}","{material}")"""
    try:
        engine.execute(query)
    except Exception as e:
        print(f"Error {e}")
    print(f"Done from {question} material {material} ")
    return obj


@app.post("/files/")
async def create_file(
    file: UploadFile = File(...),
):
    """Upload file

    Args:
        file (UploadFile)

    Returns:
        fineName: fineName
        fileItemSize: item count
    """
    fileName = "{}-{}".format(getTimeStap(), file.filename)
    with open(fileName, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    uploadedFile = convertUploadedFileJson(fileName, file.filename)
    numberOfItem = insertIntoDB(uploadedFile)
    if os.path.exists(fileName):
        os.remove(fileName)
    else:
        print("Can not delete the file as it doesn't exists")
    return {"fineName": file.filename, "NumberOfQuestions": numberOfItem}


if __name__ == "__main__":
    uvicorn.run(app, port=appPort, host=appHost)
