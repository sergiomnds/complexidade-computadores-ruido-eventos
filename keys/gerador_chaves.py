import cv2
import numpy as np
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class FalhaGeracaoDeChaves(Exception):
    pass


class GeradorDeAleatoriedadeReal:
    def __init__(self, caminho_video):
        self.cap = cv2.VideoCapture(caminho_video)
        if not self.cap.isOpened():
            raise FalhaGeracaoDeChaves(
                f"Falha de inicialização ao abrir o vídeo: {caminho_video}")

    def proximo_quadro(self):
        ret, frame = self.cap.read()
        if not ret:
            raise FalhaGeracaoDeChaves("Falha ao capturar o quadro.")
        return frame

    def proxima_imagem(self):
        tentativas = 0
        max_tentativas = 20
        while tentativas < max_tentativas:
            tentativas += 1
            try:
                return self.proximo_quadro()
            except FalhaGeracaoDeChaves:
                continue
        raise FalhaGeracaoDeChaves("Falha ao capturar uma imagem válida.")

    def get_aleatoriedade(self):
        imagem = self.proxima_imagem()
        imagem_bytes = imagem.tobytes()
        return np.frombuffer(imagem_bytes, dtype=np.uint8)

    def finalizar(self):
        self.cap.release()


class GeradorDeChaves:
    def __init__(self, gerador_de_aleatoriedade, tamanho_chave=2048):
        self.gerador_de_aleatoriedade = gerador_de_aleatoriedade
        self.tamanho_chave = tamanho_chave

    def gerar_chaves(self):
        aleatoriedade = self.gerador_de_aleatoriedade.get_aleatoriedade()
        np.random.seed(aleatoriedade.sum())
        chave_privada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.tamanho_chave,
            backend=default_backend()
        )
        chave_publica = chave_privada.public_key()
        return chave_privada, chave_publica

    def salvar_chaves(self, chave_privada, chave_publica, caminho_privado, caminho_publico):
        with open(caminho_privado, "wb") as priv_file:
            priv_file.write(chave_privada.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(caminho_publico, "wb") as pub_file:
            pub_file.write(chave_publica.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def finalizar(self):
        self.gerador_de_aleatoriedade.finalizar()
