'''
Menu de opções para o usuário escolher o que deseja fazer. O programa só é encerrado quando o usuário escolhe a opção 6 - Sair.
Utiliza o try/except para tratar o erro de digitação do usuário, caso ele digite uma opção inválida.
Utiliza as funções importadas do arquivo funcoes.py.

Autor: Sérgio Mendes
'''
from funcoes import dadosCrescente, listaLeitura, listaEventos
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from encriptador import Encriptador, gerarDados, processarDados, enviarDados

dados = gerarDados()
trios = processarDados(dados, 90.0)
enviarDados(trios)
print('Bem vindo ao Sistema de Monitoramento de Ruído de Eventos!!')
print('O total de 10 Eventos já foram gerados com sucesso! Se desejar gerar NOVOS dados, escolha a opção 1 no menu. \n')

try:
    while True:
        print("Escolha uma opção:")
        print("1 - Gerar dados aleatórios")
        print("2 - Imprimir lista de eventos monitorados")
        print("3 - Imprimir as leituras por evento monitorado")
        print("4 - Ordenar os dados em ordem crescente")
        print("5 - Sair")
        try:
            opcao = int(input("Opção escolhida: "))
        except ValueError:
            print("Opção inválida. Tente novamente.")
            continue

        if opcao == 1:
            dados = gerarDados()
            trios = processarDados(dados, 90.0)
            enviarDados(trios)
            print("Dados gerados com sucesso! \n")
        elif opcao == 2:
            listaEventos()
        elif opcao == 3:
            listaLeitura()
        elif opcao == 4:
            dadosCrescente()
        elif opcao == 5:
            print(
                '\nObrigado por utilizar o Sistema de Monitoramento de Ruído de Eventos!!')
            break
        else:
            print("Opção inválida. Tente novamente. \n")
except KeyboardInterrupt:
    print('\nPrograma interrompido pelo usuário. Encerrando...')
