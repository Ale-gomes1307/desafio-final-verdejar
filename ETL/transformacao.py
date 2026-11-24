

from datetime import datetime
from decimal import Decimal


# A2 - Padronizar estado dos clientes - ok 

def padronizar_estado(cliente):
    cliente_tratado = cliente.copy()

    cliente_tratado["estado"] = cliente_tratado["estado"].upper()

    return cliente_tratado


# A1 - Tratar clientes sem e-mail - ok

def tratar_clientes(clientes):
    clientes_tratados = []
    emails_ausentes = 0

    for cliente in clientes:
        cliente_tratado = padronizar_estado(cliente)

        if cliente_tratado["email"] is None:
            emails_ausentes += 1

        clientes_tratados.append(cliente_tratado)

    return clientes_tratados, emails_ausentes


# A3 - Converter datas - ok

def converter_data(data):
    formatos = ["%Y-%m-%d", "%d/%m/%Y"]

    for formato in formatos:
        try:
            return datetime.strptime(data, formato).date()

        except ValueError:
            continue

    raise ValueError(f"Formato de data inválido: {data}")


# A4 - Converter valores monetários - ok

def converter_valor(valor):
    valor = str(valor)
    valor = valor.replace(",", ".")

    return Decimal(valor).quantize(Decimal("0.01"))


# A5 - Remover pedidos duplicados - ok

def remover_duplicados(pedidos):
    pedidos_unicos = []
    ids_encontrados = set()
    total_duplicados = 0

    for pedido in pedidos:
        id_pedido = pedido["id"]

        if id_pedido not in ids_encontrados:
            pedidos_unicos.append(pedido)
            ids_encontrados.add(id_pedido)

        else:
            total_duplicados += 1

    return pedidos_unicos, total_duplicados


# A6 - Calcular o valor total dos itens - ok

def calcular_valor_itens(itens):
    total = Decimal("0.00")

    for item in itens:
        quantidade = item["quantidade"]
        preco = converter_valor(item["preco_unitario"])

        subtotal = quantidade * preco
        total += subtotal

    return total


# A6 - Verificar divergência entre pedido e itens -ok

def verificar_divergencia(valor_total, valor_itens):
    diferenca = abs(valor_total - valor_itens)

    return diferenca > Decimal("0.01")


# A3, A4, A5 e A6 - Tratar pedidos - ok

def tratar_pedidos(pedidos):
    pedidos_unicos, total_duplicados = remover_duplicados(pedidos)

    pedidos_tratados = []
    total_divergentes = 0

    for pedido in pedidos_unicos:
        pedido_tratado = pedido.copy()

        # A3 - Converter data
        pedido_tratado["data_pedido"] = converter_data(
            pedido_tratado["data_pedido"]
        )

        # A4 - Converter valor total
        pedido_tratado["valor_total"] = converter_valor(
            pedido_tratado["valor_total"]
        )

        # A6 - Calcular valor dos itens
        pedido_tratado["valor_itens"] = calcular_valor_itens(
            pedido_tratado["itens"]
        )

        # A6 - Verificar divergência
        pedido_tratado["divergente"] = verificar_divergencia(
            pedido_tratado["valor_total"],
            pedido_tratado["valor_itens"]
        )

        if pedido_tratado["divergente"]:
            total_divergentes += 1

        pedidos_tratados.append(pedido_tratado)

    return pedidos_tratados, total_duplicados, total_divergentes


# TESTES TEMPORÁRIOS

# Teste de clientes

clientes_teste = [
    {"nome": "Maria", "email": None, "estado": "rj"},
    {"nome": "João", "email": "joao@email.com", "estado": "sp"}
]

clientes, ausentes = tratar_clientes(clientes_teste)

print("CLIENTES:")
print(clientes)
print("E-mails ausentes:", ausentes)


# Teste de pedidos

pedidos_teste = [
    {
        "id": 101,
        "data_pedido": "2026-02-19",
        "valor_total": "63,76",
        "itens": [
            {"produto_id": 4, "quantidade": 2, "preco_unitario": "5,00"},
            {"produto_id": 2, "quantidade": 1, "preco_unitario": "53,76"}
        ]
    },
    {
        "id": 102,
        "data_pedido": "19/02/2026",
        "valor_total": "100,00",
        "itens": [
            {"produto_id": 4, "quantidade": 2, "preco_unitario": "5,00"}
        ]
    },
    {
        "id": 101,
        "data_pedido": "2026-02-19",
        "valor_total": "63,76",
        "itens": [
            {"produto_id": 4, "quantidade": 2, "preco_unitario": "5,00"},
            {"produto_id": 2, "quantidade": 1, "preco_unitario": "53,76"}
        ]
    }
]

pedidos, duplicados, divergentes = tratar_pedidos(pedidos_teste)

print("\nPEDIDOS:")
print(pedidos)
print("Total de pedidos únicos:", len(pedidos))
print("Duplicidades removidas:", duplicados)
print("Pedidos divergentes:", divergentes)


# Teste isolado do cálculo dos itens

itens_teste = [
    {"produto_id": 4, "quantidade": 6, "preco_unitario": 5.67},
    {"produto_id": 2, "quantidade": 4, "preco_unitario": 4.30},
    {"produto_id": 11, "quantidade": 3, "preco_unitario": 4.18}
]

total = calcular_valor_itens(itens_teste)

print("\nValor dos itens:", total)


# Testes isolados de divergência

print("\nTeste sem divergência:")
print(verificar_divergencia(
    Decimal("63.76"),
    Decimal("63.76")
))

print("\nTeste com divergência:")
print(verificar_divergencia(
    Decimal("63.76"),
    Decimal("63.78")
))
