from fastapi import FastAPI

from graph import graph

app = FastAPI()


@app.get("/")
def read_root():
    return graph.invoke({"rawText": "hola mundo, esto es un test mal ascrito"})


