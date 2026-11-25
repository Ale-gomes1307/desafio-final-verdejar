# Desafio Final — ETL Verdejar

## 1. Sobre o projeto

Este projeto implementa um processo ETL (Extração, Transformação e Carga) para os dados da empresa fictícia Verdejar.

O objetivo é extrair dados de uma API, realizar tratamentos e validações e carregar as informações em um banco de dados PostgreSQL, garantindo a qualidade e a consistência dos dados.

## 2. Tecnologias utilizadas

- Python
- PostgreSQL 19
- SQL
- CSV
- Requests
- Psycopg
- Pytest

## 3. Estrutura do projeto

- `ETL/`: scripts de extração, transformação, conexão e carga.
- `insumos/`: arquivos e recursos fornecidos para o desafio.
- `tests/`: testes automatizados.
- `brutos/`: dados extraídos da API.
- `consultas_validacao.sql`: consultas SQL para validação dos dados.
- `CONTRATO_DE_DADOS.md`: contrato e regras de transformação.

## 4. Resultados da execução

| Indicador | Resultado |
|---|---:|
| Clientes processados | 1.000 |
| Produtos carregados | 12 |
| Pedidos extraídos | 5.100 |
| Pedidos duplicados identificados | 100 |
| Pedidos únicos carregados | 5.000 |
| Itens de pedidos carregados | 12.455 |
| Clientes sem e-mail | 81 |
| Estados corrigidos | 151 |
| Datas convertidas | 1.037 |
| Valores monetários convertidos | 1.255 |
| Pedidos divergentes | 238 |

### Reconciliação financeira

A soma dos valores dos itens foi comparada com a soma dos respectivos subtotais calculados.

**Diferença encontrada: R$ 0,00.**

A soma das vendas mensais também foi comparada com o total geral de vendas, resultando em R$ 312.047,75.

## 5. Testes automatizados

Os testes foram implementados utilizando Pytest.

Para executar:

```bash
python -m pytest -v
```

Resultado da execução:

```text
10 passed
```

## 6. Consultas SQL

O arquivo `consultas_validacao.sql` contém consultas para:

- Vendas por mês.
- Quantidade de pedidos por estado.
- Identificação de pedidos divergentes.

## 7. Como executar o projeto

### 7.1 Pré-requisitos

- Python instalado.
- PostgreSQL instalado.
- Git instalado.

### 7.2 Instalação das dependências

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install requests "psycopg[binary]" python-dotenv pytest
```

### 7.3 Configuração do banco de dados

Crie um banco de dados chamado `verdejar` no PostgreSQL e execute o script `insumos/schema.sql`.

Configure as variáveis de ambiente no arquivo `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=verdejar
DB_USER=postgres
DB_PASSWORD=sua_senha
```

Não compartilhe o arquivo `.env` com suas credenciais.

### 7.4 Inicialização da API

Em um terminal, execute:

```bash
python insumos/api_verdejar.py --dados insumos/dados
```

### 7.5 Execução do ETL

Em outro terminal, execute:

```bash
python -m ETL.carga
```

### 7.6 Execução dos testes

```bash
python -m pytest -v
```

### 7.7 Validação dos dados

As consultas SQL de validação estão disponíveis no arquivo `consultas_validacao.sql`.

## 8. Idempotência

O processo utiliza `ON CONFLICT DO NOTHING` nas operações de inserção para evitar a duplicação de registros já existentes.

A idempotência foi validada por meio de uma nova execução do ETL, mantendo as quantidades de registros nas tabelas do banco de dados.

## 9. Considerações finais

O projeto permitiu aplicar conceitos de Engenharia de Dados, incluindo extração via API, transformação e padronização de dados, tratamento de duplicidades, validação de valores financeiros, carga em banco relacional e testes automatizados.