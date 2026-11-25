
from datetime import date
from decimal import Decimal

from ETL.transformacao import (
    converter_data,
    converter_valor,
    remover_duplicados,
    tratar_clientes,
    padronizar_estado,
    verificar_divergencia,
)

# função de teste para a função converter_data, verificando se a conversão de datas está correta
def test_converter_data_formato_brasileiro():
    resultado, precisou_converter = converter_data("19/02/2026")

    assert resultado == date(2026, 2, 19)
    assert precisou_converter is True

def test_converter_data_formato_iso():
    resultado, precisou_converter = converter_data("2026-02-19")

    assert resultado == date(2026, 2, 19)
    assert precisou_converter is False

# função de teste para a função converter_valor, verificando se a conversão de valores monetários está correta

def test_converter_valor_com_virgula():
    resultado, precisou_converter = converter_valor("125,50")

    assert resultado == Decimal("125.50")
    assert precisou_converter is True

# função de teste para a função remover_duplicados, verificando se os pedidos duplicados são removidos corretamente

def test_remover_pedidos_duplicados():
    pedidos = [
        {"id": 1, "valor": 100},
        {"id": 2, "valor": 200},
        {"id": 1, "valor": 100},
    ]

    resultado, total_duplicados = remover_duplicados(pedidos)

    assert len(resultado) == 2
    assert total_duplicados == 1
    assert resultado[0]["id"] == 1
    assert resultado[1]["id"] == 2



def test_converter_data_formato_invalido():
    try:
        converter_data("35/02/2026")
        assert False, "Era esperado um ValueError"
    except ValueError:
        assert True

# função de teste para a função tratar_clientes, verificando se os clientes sem email são tratados corretamente
def test_tratar_cliente_sem_email():
    clientes = [
        {"nome": "Maria", "email": None, "estado": "rj"}
    ]

    resultado, emails_ausentes, estados_corrigidos = tratar_clientes(clientes)

    assert len(resultado) == 1
    assert resultado[0]["email"] is None
    assert emails_ausentes == 1
    assert estados_corrigidos == 1


# função de teste para a função padronizar_estado, verificando se o estado é padronizado corretamente

def test_padronizar_estado():
     cliente = {"nome": "Maria", "email": "maria@email.com", "estado": "rj"}

     resultado = padronizar_estado(cliente)

     assert resultado["estado"] == "RJ"

# função de teste para a função verificar_divergencia, verificando se a divergência entre valores é detectada corretamente

def test_verificar_pedido_sem_divergencia():
    resultado = verificar_divergencia(
        Decimal("63.76"),
        Decimal("63.76")
    )

    assert resultado is False


def test_verificar_pedido_com_divergencia():
    resultado = verificar_divergencia(
        Decimal("63.76"),
        Decimal("63.78")
    )

    assert resultado is True

def test_verificar_diferenca_de_um_centavo():
    resultado = verificar_divergencia(
        Decimal("100.00"),
        Decimal("100.01")
    )

    assert resultado is False