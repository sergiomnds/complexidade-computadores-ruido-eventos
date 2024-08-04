import shutil
from gerador_chaves import FalhaGeracaoDeChaves, GeradorDeAleatoriedadeReal, GeradorDeChaves


if __name__ == "__main__":
    caminho_video = "keys/comedouro.mp4"
    gerador_aleatoriedade = GeradorDeAleatoriedadeReal(caminho_video)
    gerador_chaves = GeradorDeChaves(gerador_aleatoriedade)

    try:
        chave_privada, chave_publica = gerador_chaves.gerar_chaves()
        gerador_chaves.salvar_chaves(
            chave_privada, chave_publica, "chave_privada.pem", "chave_publica.pem")
        destino_pasta_servidor = "server/chave_privada.pem"
        shutil.copy('chave_privada.pem', destino_pasta_servidor)
    except FalhaGeracaoDeChaves as e:
        print(f"Erro: {e}")
    finally:
        gerador_chaves.finalizar()
