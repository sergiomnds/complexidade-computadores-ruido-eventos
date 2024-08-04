from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import base64
import requests
import random
import threading
import os


class Encriptador:
    def __init__(self, chave_publica_path):
        # Verifica se o caminho é uma string e se o arquivo existe
        if not isinstance(chave_publica_path, str):
            raise ValueError(
                "O caminho para a chave pública deve ser uma string.")
        try:
            with open(chave_publica_path, "rb") as chave_publica_file:
                self.chave_publica = serialization.load_pem_public_key(
                    chave_publica_file.read(),
                    backend=default_backend()
                )
        except Exception as e:
            raise FileNotFoundError(
                f"Falha ao carregar a chave pública: {str(e)}")

    def encriptar(self, dados):
        try:
            dados_bytes = dados.encode('utf-8')
            cifragem = self.chave_publica.encrypt(
                dados_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return base64.b64encode(cifragem).decode('utf-8')
        except Exception as e:
            raise Exception(f"Falha ao encriptar dados: {str(e)}")


def gerarDados(qntEventos=10):
    def gerar_ruido(evento_id, buffer, lock):
        ruido = round(random.uniform(40.0, 140.0), 1)
        with lock:
            buffer.append({"id": evento_id, "ruido": ruido})

    threads = []
    lock = threading.Lock()
    buffer = []

    for i in range(1, qntEventos + 1):
        thread = threading.Thread(target=gerar_ruido, args=(i, buffer, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if os.path.exists('client/eventos.txt'):
        os.remove('client/eventos.txt')

    with open('client/eventos.txt', 'w') as arquivo:
        for evento in buffer:
            arquivo.write(f'EVENTO {evento["id"]}: {evento["ruido"]} \n')

    return buffer


def processarDados(eventos, limiteRuido=90.0):
    def trioRuido(eventos, limiteRuido=90.0):
        encontrados = []
        n = len(eventos)
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    if eventos[i]["ruido"] > limiteRuido and eventos[j]["ruido"] > limiteRuido and eventos[k]["ruido"] > limiteRuido:
                        encontrados.append(
                            (eventos[i]["id"], eventos[j]["id"], eventos[k]["id"]))
        return encontrados

    trios = trioRuido(eventos, limiteRuido)
    return trios


def enviarDados(trios, server_url="http://localhost:8000/trios/", chave_publica='chave_publica.pem'):
    encriptador = Encriptador(chave_publica)
    trios_encriptados = []

    for trio in trios:
        trio_str = ','.join(map(str, trio))
        trio_encriptado = encriptador.encriptar(trio_str)
        trios_encriptados.append({"eventos": trio_encriptado})

    response = requests.post(server_url, json=trios_encriptados)
    if response.status_code == 200:
        print("Trios enviados com sucesso!")
    else:
        print(f"Erro ao enviar trios: {response.status_code}")
