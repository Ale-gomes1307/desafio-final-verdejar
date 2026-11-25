# Como usei IA

Durante o desenvolvimento do desafio ETL Verdejar, utilizei inteligência artificial como ferramenta de apoio para compreender conceitos, revisar códigos, identificar erros e propor melhorias na implementação.

As sugestões foram avaliadas considerando os requisitos do desafio e validadas por meio de testes automatizados e consultas no PostgreSQL.

## 1. Sugestões aceitas

### 1.1 Organização do processo de carga

A IA sugeriu organizar a carga dos dados em funções separadas para produtos, clientes, pedidos e itens dos pedidos.

**Motivo da aceitação:** a separação tornou o código mais organizado, facilitou a manutenção e permitiu compreender melhor cada etapa do processo ETL.

**Validação:** execução do processo de carga e conferência das quantidades diretamente no PostgreSQL.

### 1.2 Conversão de datas com identificação de alterações

A IA sugeriu modificar a função `converter_data()` para retornar, além da data convertida, um indicador informando se houve necessidade de conversão.

**Motivo da aceitação:** essa abordagem permitiu contabilizar quantas datas precisaram ser padronizadas durante o processamento.

**Validação:** testes automatizados para os formatos brasileiro e ISO, além da execução completa do ETL. Foram identificadas 1.037 datas convertidas.

## 2. Sugestões rejeitadas

### 2.1 Realizar o commit a cada registro inserido

Durante a revisão da função de carga, foi considerada a possibilidade de confirmar a transação dentro do laço `for`.

**Motivo da rejeição:** realizar o commit a cada registro seria desnecessário e aumentaria a quantidade de operações no banco de dados.

**Alternativa adotada:** realizar o commit após o processamento de todos os registros, mantendo o rollback em caso de erro.

### 2.2 Contabilizar novamente os valores monetários na etapa de carga

Foi considerada a possibilidade de contabilizar as conversões dos preços dos itens novamente dentro da função de inserção no banco.

**Motivo da rejeição:** os valores já eram contabilizados durante a transformação, em `calcular_valor_itens()`. Fazer uma segunda contagem poderia gerar indicadores duplicados.

**Alternativa adotada:** manter a responsabilidade de contabilização na etapa de transformação e utilizar somente o valor convertido durante a inserção no banco.

## 3. Falhas e retrabalho

### 3.1 Incompatibilidade entre a função de conversão e os testes

Durante a implementação, a função `converter_data()` foi modificada para retornar dois valores: a data convertida e um indicador booleano.

Inicialmente, os testes automatizados ainda esperavam receber somente a data, causando duas falhas.

**Correção:** os testes foram atualizados para validar tanto a data quanto o indicador de conversão.

### 3.2 Erro de indentação na função de carga

Durante a organização do arquivo `carga.py`, um bloco `try` ficou fora da função `inserir_produtos()`, causando uma estrutura incorreta no código.

**Correção:** a indentação foi ajustada e o arquivo foi validado utilizando `py_compile`.

## 4. Validação das implementações

As alterações sugeridas pela IA foram verificadas por meio de:

- Testes automatizados com Pytest.
- Verificação de sintaxe com `py_compile`.
- Execução completa do processo ETL.
- Consultas SQL no PostgreSQL.
- Conferência da quantidade de registros carregados.
- Validação da reconciliação financeira.

Resultado final dos testes: **10 testes aprovados**.

A execução do ETL identificou 100 pedidos duplicados, 238 pedidos divergentes, 1.037 datas convertidas e 1.255 valores monetários convertidos.

A idempotência também foi validada por meio de uma nova execução, mantendo as quantidades de registros nas tabelas do banco de dados.

## 5. Considerações finais

A inteligência artificial foi utilizada como ferramenta de apoio durante o desenvolvimento, mas as decisões de implementação foram avaliadas e verificadas por meio de testes e consultas.

O processo contribuiu para o aprendizado de Python, organização de funções, tratamento de dados, testes automatizados e integração com PostgreSQL.