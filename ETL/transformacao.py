

from datetime import datetime
from decimal import Decimal


# A2 - Padronizar estado dos clientes - ok 

def padronizar_estado(cliente):
    cliente_tratado = cliente.copy()

    cliente_tratado["estado"] = cliente_tratado["estado"].upper()

    return cliente_tratado


# A1 e A2 - Tratar clientes

def tratar_clientes(clientes):
    clientes_tratados = []
    emails_ausentes = 0
    estados_corrigidos = 0

    for cliente in clientes:

        if cliente["estado"] != cliente["estado"].upper():
            estados_corrigidos += 1

        cliente_tratado = padronizar_estado(cliente)

        if cliente_tratado["email"] is None:
            emails_ausentes += 1

        clientes_tratados.append(cliente_tratado)

    return clientes_tratados, emails_ausentes, estados_corrigidos

# A3 - Converter datas - ok

def converter_data(data):
    formatos = ["%Y-%m-%d", "%d/%m/%Y"]

    for formato in formatos:
        try:
            data_convertida = datetime.strptime(data, formato).date()

            return data_convertida, formato != "%Y-%m-%d"

        except ValueError:
            continue

    raise ValueError(f"Formato de data inválido: {data}")


# A4 - Converter valores monetários - ok

def converter_valor(valor):
    valor = str(valor)

    precisou_converter = "," in valor

    valor = valor.replace(",", ".")

    valor_convertido = Decimal(valor).quantize(Decimal("0.01"))

    return valor_convertido, precisou_converter



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
    valores_convertidos = 0

    for item in itens:
        quantidade = item["quantidade"]

        preco, precisou_converter = converter_valor(
            item["preco_unitario"]
        )

        if precisou_converter:
            valores_convertidos += 1

        subtotal = quantidade * preco
        total += subtotal

    return total, valores_convertidos


# A6 - Verificar divergência entre pedido e itens -ok

def verificar_divergencia(valor_total, valor_itens):
    diferenca = abs(valor_total - valor_itens)

    return diferenca > Decimal("0.01")


# A3, A4, A5 e A6 - Tratar pedidos - ok

def tratar_pedidos(pedidos):
    pedidos_unicos, total_duplicados = remover_duplicados(pedidos)

    pedidos_tratados = []
    total_divergentes = 0
    total_datas_convertidas = 0
    total_valores_convertidos = 0

    for pedido in pedidos_unicos:
        pedido_tratado = pedido.copy()

        # A3 - Converter data
        data_convertida, precisou_converter = converter_data(
            pedido_tratado["data_pedido"]
        )

        pedido_tratado["data_pedido"] = data_convertida

        if precisou_converter:
            total_datas_convertidas += 1

        # A4 - Converter valor total
        valor_total, precisou_converter = converter_valor(
            pedido_tratado["valor_total"]
        )

        pedido_tratado["valor_total"] = valor_total

        if precisou_converter:
            total_valores_convertidos += 1

        # A6 - Calcular valor dos itens
        valor_itens, valores_convertidos = calcular_valor_itens(
            pedido_tratado["itens"]
        )

        pedido_tratado["valor_itens"] = valor_itens

        total_valores_convertidos += valores_convertidos

        # A6 - Verificar divergência
        pedido_tratado["divergente"] = verificar_divergencia(
            pedido_tratado["valor_total"],
            pedido_tratado["valor_itens"]
        )

        if pedido_tratado["divergente"]:
            total_divergentes += 1

        pedidos_tratados.append(pedido_tratado)

    return (
        pedidos_tratados,
        total_duplicados,
        total_divergentes,
        total_datas_convertidas,
        total_valores_convertidos
    )
