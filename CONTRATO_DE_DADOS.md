# Contrato de Dados — ETL Verdejar

## 1. Objetivo

Este documento define os campos, tipos, regras de nulabilidade e transformações aplicadas aos dados da Verdejar durante o processo ETL.

O objetivo é garantir que os dados provenientes da API e do arquivo CSV estejam padronizados, consistentes e adequados para armazenamento no PostgreSQL.

## 2. Fontes de dados

| Fonte | Dados |
|---|---|
| API `/clientes` | Cadastro de clientes |
| API `/pedidos` | Pedidos e seus itens |
| `produtos.csv` | Catálogo de produtos |

## 3. Estrutura e regras das tabelas

### 3.1 Tabela: clientes

| Campo | Tipo PostgreSQL | Aceita NULL? | Regra |
|---|---|---|---|
| id | INTEGER | Não | Identificador único do cliente. |
| nome | TEXT | Não | Manter o nome recebido da origem. |
| email | TEXT | Sim | Manter NULL quando o e-mail estiver ausente. |
| cidade | TEXT | Não | Manter a cidade recebida da origem. |
| estado | CHAR(2) | Não | Padronizar a sigla para letras maiúsculas. |
| cadastro_em | DATE | Não | Converter para o tipo DATE. |

**Chave primária:** `id`.

### 3.2 Tabela: produtos

| Campo | Tipo PostgreSQL | Aceita NULL? | Regra |
|---|---|---|---|
| produto_id | INTEGER | Não | Identificador único do produto. |
| nome | TEXT | Não | Manter o nome recebido do CSV. |
| categoria | TEXT | Não | Manter a categoria recebida do CSV. |
| preco_base | NUMERIC(10,2) | Não | Armazenar o preço com duas casas decimais. |

**Chave primária:** `produto_id`.

### 3.3 Tabela: pedidos

| Campo | Tipo PostgreSQL | Aceita NULL? | Regra |
|---|---|---|---|
| id | INTEGER | Não | Identificador único do pedido. Remover duplicados, mantendo a primeira ocorrência. |
| cliente_id | INTEGER | Não | Deve corresponder a um cliente cadastrado. |
| data_pedido | DATE | Não | Converter os formatos AAAA-MM-DD e DD/MM/AAAA para DATE. |
| status | TEXT | Não | Manter o status recebido da origem. |
| valor_total | NUMERIC(12,2) | Não | Converter números e textos com vírgula decimal para valor numérico com duas casas decimais. |
| valor_itens | NUMERIC(12,2) | Não | Calcular pela soma de quantidade multiplicada pelo preço unitário de cada item. |
| divergente | BOOLEAN | Não | Marcar TRUE quando a diferença entre valor_total e valor_itens for maior que R$ 0,01; caso contrário, FALSE. |

**Chave primária:** `id`.

**Chave estrangeira:** `cliente_id` referencia `clientes(id)`.

### 3.4 Tabela: itens_pedido

| Campo | Tipo PostgreSQL | Aceita NULL? | Regra |
|---|---|---|---|
| pedido_id | INTEGER | Não | Deve corresponder a um pedido cadastrado. |
| linha | INTEGER | Não | Identifica a linha do item dentro do pedido. |
| produto_id | INTEGER | Não | Deve corresponder a um produto cadastrado. |
| quantidade | INTEGER | Não | Manter a quantidade recebida da origem. |
| preco_unitario | NUMERIC(10,2) | Não | Armazenar o preço unitário com duas casas decimais. |

**Chave primária composta:** `pedido_id` e `linha`.

**Chaves estrangeiras:**
- `pedido_id` referencia `pedidos(id)`.
- `produto_id` referencia `produtos(produto_id)`.

## 4. Regras de qualidade dos dados

O ETL deverá tratar as seis armadilhas declaradas no desafio:

| Código | Problema | Tratamento esperado |
|---|---|---|
| A1 | E-mails ausentes | Manter o cliente e gravar email como NULL. |
| A2 | Estados em maiúsculas e minúsculas | Converter todas as siglas para maiúsculas. |
| A3 | Datas em formatos diferentes | Converter para DATE. |
| A4 | Valores numéricos ou textos com vírgula decimal | Converter para NUMERIC com duas casas decimais. |
| A5 | Pedidos duplicados | Manter apenas a primeira ocorrência de cada ID. |
| A6 | Divergência entre total do pedido e soma dos itens | Calcular valor_itens e identificar pedidos divergentes. |

## 5. Regras de integridade e carga

- Respeitar as chaves primárias e estrangeiras do esquema PostgreSQL.
- Carregar os dados na ordem: produtos, clientes, pedidos e itens_pedido.
- Garantir que executar o ETL novamente não duplique os registros.
- Utilizar consultas parametrizadas na inserção dos dados.

## 6. Monitoramento e validação

O processo deverá imprimir contadores para acompanhar a qualidade dos dados:

- Quantidade de e-mails nulos.
- Quantidade de estados padronizados.
- Quantidade de datas convertidas.
- Quantidade de valores convertidos.
- Quantidade de pedidos duplicados descartados.
- Quantidade de pedidos divergentes.

A reconciliação deverá comparar as contagens e somas dos dados de origem com os dados carregados no PostgreSQL.
