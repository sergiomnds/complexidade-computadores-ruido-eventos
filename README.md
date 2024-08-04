![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

[![Status](https://img.shields.io/badge/Status-Concluído-blue)]()

<h1 align="center">🔊 Monitoramento de Ruído de Eventos (com Threads)</h1>

Repositório dedicado ao programa desenvolvido para a III Avaliação da disciplina Complexidade de Algoritmos.

O programa gera um ruído aleatório de 10 eventos diferentes e os guarda em arquivo de texto. Com base nisso, ele possue as seguintes funcionalidades:

- Gerar NOVOS dados para os eventos;
- Processar os dados (maior complexidade) e enviar o resultado a um servidor;
- Listar os eventos monitorados;
- Listar as leituras de todos os eventos que foram monitorados;
- Listar os eventos em ordem crescente, pela ruído;

Para realizar o envio dos dados eles são criptografados com uma fonte de aleatoriedade, e depois descriptografados ao serem recebidos.

<h2>🐍 Python</h2>
O programa foi desenvolvido inteiramente em Python, e deve está instalado na máquina do usuário para funcionar corretamente.

IMPORTANTE: O Interpretor deve está atualizado! Para o desenvolvimento deste programa foi utilizado o Python 3.11.2 64-bit. Recomendo usar esta versão ou superior!

<h2>🏃 Como rodar a aplicação?</h2>

1º Faça a instalação das dependências rodando o comando:

```
pip install -r requirements.txt
```

2º Rode o 'main.py' dentro da pasta 'keys' para gerar as chaves privadas e públicas

3º Vamos abrir um terminal e ir até a pasta do servidor:

```
cd server
```

4º Agora vamos iniciar o servidor:

```
uvicorn main:app --reload
```

5º Por último, abra um NOVO terminal e rode o 'main.py' da pasta 'client'.

6º Ao rodar, automaticamente serão enviados os dados ao servidor que podem ser vistos ao colocar a rota "/trios/". Ex: http://127.0.0.1:8000/trios/
