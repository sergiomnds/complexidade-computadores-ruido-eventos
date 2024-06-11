from typing import List, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Evento(BaseModel):
    id: int
    ruido: float

eventos_acumulados = []
trios_encontrados = []

@app.post("/eventos/")
def receber_eventos(eventos: List[Evento]):
    eventos_acumulados.extend(eventos)
    return {"message": "Eventos recebidos com sucesso!"}

@app.get("/processar/")
def processar_eventos(limiteRuido: float = 90.0):
    def trioRuido(eventos, limiteRuido=90.0):
        encontrados = []
        n = len(eventos)
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    if eventos[i].ruido > limiteRuido and eventos[j].ruido > limiteRuido and eventos[k].ruido > limiteRuido:
                        encontrados.append(
                            (eventos[i].id, eventos[j].id, eventos[k].id))
        return encontrados

    if not eventos_acumulados:
        raise HTTPException(status_code=404, detail="Nenhum evento acumulado")
    
    trios = trioRuido(eventos_acumulados, limiteRuido)
    
    if not trios:
        return {"message": f"Não foi encontrado nenhum trio de eventos com ruído acima de {limiteRuido} dB."}
    
    # Limpa a lista de trios encontrados
    trios_encontrados.clear()
    trios_encontrados.extend(trios)
    
    # Limpa a lista de eventos acumulados
    eventos_acumulados.clear()
    
    return {"trios": trios}
