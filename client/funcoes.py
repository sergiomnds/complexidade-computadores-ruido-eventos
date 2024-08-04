'''
Arquivo com as funções utilizadas no programa principal.
Cada função possui uma breve descrição de sua funcionalidade e complexidade.

Autor: Sérgio Mendes
'''


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
    with open('client/eventos.txt', 'r') as arquivo:
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
    with open('client/eventos.txt', 'r') as arquivo:
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
    with open('client/eventos.txt', 'r') as arquivo:
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
