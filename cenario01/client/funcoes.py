'''
Arquivo com as funções utilizadas no programa principal.
Cada função possui uma breve descrição de sua funcionalidade e complexidade.

Autor: Sérgio Mendes
'''
import random
import threading
import requests

def gerarDados(qntEventos=10, server_url="http://localhost:8000/eventos/"):
    '''
    Função que gera ruídos aleatórios para os eventos com Threads, envia para o servidor e salva em um arquivo.

    :param qntEventos: quantidade de eventos que serão gerados. Por padrão são gerados 10 eventos.
    :type qntEventos: int
    :param server_url: URL do servidor para onde os eventos serão enviados.
    :type server_url: str

    :complexidade: O(n), onde n é a quantidade de eventos que serão gerados. A medida que a lista cresce, o algoritmo cresce de forma linear quanto a suas operações.
    Se a entrada de dados for muito grande, a execução do algoritmo pode levar muito tempo e exigir muita memória.
    '''

    # Função para gerar ruído de um evento e adicionar ao buffer central
    def gerar_ruido(evento_id, buffer, lock):
        ruido = round(random.uniform(40.0, 140.0), 1)
        with lock:
            buffer.append({"id": evento_id, "ruido": ruido})

    # Lista de threads
    threads = []
    lock = threading.Lock()
    buffer = []

    # Criar e iniciar uma thread para cada evento
    for i in range(1, qntEventos + 1):
        thread = threading.Thread(target=gerar_ruido, args=(i, buffer, lock))
        threads.append(thread)
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

    # Se o arquivo já existir, ele será removido e um novo arquivo será criado.
    if os.path.exists('eventos.txt'):
        os.remove('eventos.txt')

    # Cria um arquivo e escreve os dados dos eventos
    with open('eventos.txt', 'w') as arquivo:
        for evento in buffer:
            arquivo.write(f'EVENTO {evento["id"]}: {evento["ruido"]} \n')

    # Enviar todos os dados do buffer para o servidor
    response = requests.post(server_url, json=buffer)
    if response.status_code == 200:
        print("Eventos enviados com sucesso!")
    else:
        print(f"Erro ao enviar eventos: {response.status_code}")

def listaEventos():
    '''
    Função que imprime uma lista de eventos monitorados, sem mostrar seus ruídos.

    :complexidade: O(n), onde n é a quantidade de eventos que serão impressos. A medida que a lista cresce, o algoritmo cresce de forma linear quanto a suas operações.
    Se a entrada de dados for muito grande, a execução do algoritmo pode levar muito tempo e exigir muita memória.
    '''
    # Define o cabeçalho da tabela
    cabecalho = ["ID - EVENTO"]

    # Cria uma lista de linhas da tabela
    linhas = []

    # Lê o arquivo e adiciona os dados à lista de linhas
    with open('eventos.txt', 'r') as arquivo:
        for linha in arquivo:
            evento = linha.split(":")[0].strip()
            linhas.append([evento])

    # Imprime a tabela
    print("Lista de Eventos:")
    print("-" * 20)
    print(f"{cabecalho[0]:^20}")
    print("-" * 20)
    for linha in linhas:
        print(f"{linha[0]:^20}")
    print("-" * 20)


def listaLeitura():
    '''
    Função que imprime uma lista das leituras feitas sobre os eventos monitorados, mostrando seus ruídos.

    :complexidade: O(n), onde n é a quantidade de eventos que serão impressos. A medida que a lista cresce, o algoritmo cresce de forma linear quanto a suas operações.
    Se a entrada de dados for muito grande, a execução do algoritmo pode levar muito tempo e exigir muita memória.
    '''

    # Cria uma lista de dados e adiciona os dados do arquivo à lista
    dados = []
    with open('eventos.txt', 'r') as arquivo:
        for linha in arquivo:
            evento, ruido = linha.strip().split(': ')
            dados.append((evento, ruido))

    # Imprime a tabela
    print('Ruídos dos eventos: ')
    print("-" * 40)
    print(f'{"ID - EVENTO":<20}{"RUÍDO (dB)":^20}')
    print("-" * 40)
    for dado in dados:
        print(f'{dado[0]:<20}{dado[1]:^20}')
    print("-" * 40)


def dadosCrescente():
    '''
    Função que retorna os dados em ordem crescente dentro de uma tabela.

    :complexidade: O(n²), onde n é a quantidade de eventos a serem ordenados. São dois loops que percorrem a lista, a cada iteração do loop externo, que percorre toda a lista, o loop interno percorre novamente toda a lista, comparando o elemento atual com o próximo e realizando a troca se necessário.

    Se a entrada de dados for muito grande, o tempo de execução do algoritmo pode se tornar impraticável, além de exigir uma quantidade significativa de recursos de memória.
    Por exemplo, se o algoritmo leva 1 segundo para classificar uma lista de 1000 itens, ele levaria 16 minutos para classificar uma lista de 10.000 itens, e cerca de 28 horas para classificar uma lista de 100.000 itens.
    '''

    # Lê os dados do arquivo e os adiciona à lista
    with open('eventos.txt', 'r') as arquivo:
        eventos = []
        for linha in arquivo:
            evento, ruido = linha.strip().split(': ')
            # adiciona o evento e o ruído à lista
            eventos.append((evento, float(ruido)))

    # Ordena a lista de eventos, usando bubble sort
    n = len(eventos)
    for i in range(n):
        for j in range(0, n-i-1):
            if eventos[j][1] > eventos[j+1][1]:
                eventos[j], eventos[j +
                                              1] = eventos[j+1], eventos[j]

    # Imprime a tabela ordenada
    print('Ruídos dos eventos em ordem crescente: ')
    print("-" * 40)
    print(f'{"RUÍDO (dB)":<20}{"ID - EVENTO":^20}')
    print("-" * 40)
    for evento in eventos:
        print(f'{evento[1]:^20}{evento[0]:^20}')
