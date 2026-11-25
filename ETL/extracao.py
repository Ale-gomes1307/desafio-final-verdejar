
import requests
import json
import csv

API_URL = "http://127.0.0.1:8000" 

# a função abaixo consulta a API para uma rota e página específicas, retornando os dados da resposta
def consultar_api(rota, pagina):
    url = f"{API_URL}/{rota}"

    parametros = {
        "page": pagina,
        "page_size": 50
    }

    resposta = requests.get(url, params=parametros)

    resposta.raise_for_status()

    return resposta.json()

# a função abaixo extrai todos os dados de uma rota específica da API, lidando com a paginação
def extrair_todos(rota):
    print(f"Extraindo todos os dados da rota: {rota}")
    primeira_pagina = consultar_api(rota, 1)

    todos_os_dados = primeira_pagina["items"]

    total_paginas = primeira_pagina["total_pages"]

    for pagina in range(2, total_paginas + 1):
        print(f"Extraindo {rota}: página {pagina} de {total_paginas}")
        resposta = consultar_api(rota, pagina)

        todos_os_dados.extend(resposta["items"])

    return todos_os_dados

# a função abaixo salva os dados extraídos em um arquivo JSON na pasta "brutos"
def salvar_json(nome_arquivo, dados):
    caminho = f"brutos/{nome_arquivo}.json"

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

# Extraindo todos os clientes da API
clientes = extrair_todos("clientes")

# Exibir informações sobre os clientes extraídos
print("Total extraído:", len(clientes))
print("Primeiro cliente:", clientes[0]["nome"])
print("Último cliente:", clientes[-1]["nome"])

# Extraindo todos os pedidos da API
pedidos = extrair_todos("pedidos")
print("Total de pedidos extraídos:", len(pedidos))

# Salvar os dados extraídos em arquivos JSON
salvar_json("clientes", clientes)
salvar_json("pedidos", pedidos)

print("Arquivos brutos salvos com sucesso!")

# a função abaixo lê os dados de produtos de um arquivo CSV e retorna uma lista de dicionários representando cada produto

def ler_produtos():
    caminho = "insumos/dados/produtos.csv"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        produtos = list(leitor)

    return produtos

if __name__ == "__main__":
    produtos = ler_produtos()

    print(f"Total de produtos encontrados: {len(produtos)}")
    print("Primeiro produto:")
    print(produtos[0])