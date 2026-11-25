

from ETL.conexao import conectar_banco
from ETL.transformacao import (
    tratar_clientes,
    converter_data,
    tratar_pedidos,
    converter_valor
)


# Função para inserir produtos no banco de dados

def inserir_produtos(produtos):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        for produto in produtos:
            cursor.execute(
                """
                INSERT INTO produtos (
                    produto_id,
                    nome,
                    categoria,
                    preco_base
                )
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (produto_id) DO NOTHING
                """,
                (
                    produto["produto_id"],
                    produto["nome"],
                    produto["categoria"],
                    produto["preco_base"]
                )
            )

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()


# Função para inserir clientes no banco de dados

def inserir_clientes(clientes):
    clientes_tratados, emails_ausentes, estados_corrigidos = tratar_clientes(clientes)

    conexao = conectar_banco()
    cursor = conexao.cursor()

    total_datas_convertidas_clientes = 0

    try:
        for cliente in clientes_tratados:
            cadastro_em, precisou_converter = converter_data(
                cliente["cadastro_em"]
            )

            if precisou_converter:
                total_datas_convertidas_clientes += 1

            cursor.execute(
                """
                INSERT INTO clientes (
                    id,
                    nome,
                    email,
                    cidade,
                    estado,
                    cadastro_em
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    cliente["id"],
                    cliente["nome"],
                    cliente["email"],
                    cliente["cidade"],
                    cliente["estado"],
                    cadastro_em
                )
            )

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()

    return (
        emails_ausentes,
        estados_corrigidos,
        total_datas_convertidas_clientes
    )


# Função para inserir pedidos e seus itens no banco de dados

def inserir_pedidos(pedidos):
    (
        pedidos_tratados,
        total_duplicados,
        total_divergentes,
        total_datas_convertidas,
        total_valores_convertidos
    ) = tratar_pedidos(pedidos)

    conexao = conectar_banco()
    cursor = conexao.cursor()

    try:
        for pedido in pedidos_tratados:

            # Primeiro: inserir o pedido
            cursor.execute(
                """
                INSERT INTO pedidos (
                    id,
                    cliente_id,
                    data_pedido,
                    status,
                    valor_total,
                    valor_itens,
                    divergente
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
                """,
                (
                    pedido["id"],
                    pedido["cliente_id"],
                    pedido["data_pedido"],
                    pedido["status"],
                    pedido["valor_total"],
                    pedido["valor_itens"],
                    pedido["divergente"]
                )
            )

            # Segundo: inserir os itens daquele pedido
            for linha, item in enumerate(pedido["itens"], start=1):
                cursor.execute(
                    """
                    INSERT INTO itens_pedido (
                        pedido_id,
                        linha,
                        produto_id,
                        quantidade,
                        preco_unitario
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (pedido_id, linha) DO NOTHING
                    """,
                    (
                        pedido["id"],
                        linha,
                        item["produto_id"],
                        item["quantidade"],
                        converter_valor(item["preco_unitario"])[0]
                    )
                )

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        cursor.close()
        conexao.close()

    return (
        total_duplicados,
        total_divergentes,
        total_datas_convertidas,
        total_valores_convertidos
    )


# Execução principal do processo de carga

if __name__ == "__main__":
    from ETL.extracao import ler_produtos, extrair_todos

    # Carregar produtos
    produtos = ler_produtos()
    inserir_produtos(produtos)
    print("Produtos inseridos com sucesso!")

    # Carregar clientes
    clientes = extrair_todos("clientes")

    emails_ausentes, estados_corrigidos, datas_clientes = inserir_clientes(clientes)

    print("Clientes inseridos com sucesso!")
    print(f"Clientes sem e-mail: {emails_ausentes}")
    print(f"Estados corrigidos: {estados_corrigidos}")
    print(f"Datas de cadastro convertidas: {datas_clientes}")

    # Carregar pedidos e seus itens
    pedidos = extrair_todos("pedidos")

    (
        total_duplicados,
        total_divergentes,
        total_datas_convertidas,
        total_valores_convertidos
    ) = inserir_pedidos(pedidos)

    print("Pedidos e itens inseridos com sucesso!")
    print(f"Pedidos duplicados ignorados: {total_duplicados}")
    print(f"Pedidos divergentes: {total_divergentes}")
    print(f"Datas dos pedidos convertidas: {total_datas_convertidas}")

    # Total geral de datas convertidas
    total_datas = datas_clientes + total_datas_convertidas
    print(f"Total de datas convertidas: {total_datas}")

    # Total geral de valores monetários convertidos
    print(f"Valores monetários convertidos: {total_valores_convertidos}")
