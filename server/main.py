from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

app = FastAPI()


class Trio(BaseModel):
    eventos: str


# Carregar a chave privada de um arquivo PEM
with open("chave_privada.pem", "rb") as chave_privada_file:
    chave_privada = serialization.load_pem_private_key(
        chave_privada_file.read(),
        password=None,
        backend=default_backend()
    )

trios_armazena = []


def desencriptar(dados_encriptados):
    try:
        dados_encriptados_bytes = base64.b64decode(dados_encriptados)
        dados_decriptados = chave_privada.decrypt(
            dados_encriptados_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return dados_decriptados.decode('utf-8')
    except Exception as e:
        raise Exception(f"Falha ao desencriptar dados: {str(e)}")


@app.post("/trios/")
async def receber_trios(trios: list[Trio]):
    try:
        trios_descriptografados = []
        for trio in trios:
            dados_descriptografados = desencriptar(trio.eventos)
            trios_descriptografados.append(dados_descriptografados)

        # Armazenar trios descriptografados
        trios_armazena.extend(trios_descriptografados)

        return {"status": "sucesso", "dados": trios_descriptografados}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/trios/")
async def visualizar_trios():
    try:
        if not trios_armazena:
            return {"status": "nenhum dado disponível"}
        return {"status": "sucesso", "dados": trios_armazena}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
