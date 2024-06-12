from typing import List, Tuple
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Trio(BaseModel):
    eventos: Tuple[int, int, int]

trios_acumulados = []

@app.post("/trios/")
def receber_trios(trios: List[Trio]):
    trios_acumulados.clear()
    trios_acumulados.extend(trios)
    return {"message": "Trios recebidos com sucesso!"}

@app.get("/trios/")
def obter_trios():
    if not trios_acumulados:
        return {"message": "Nenhum trio recebido"}
    return {"trios": trios_acumulados}
