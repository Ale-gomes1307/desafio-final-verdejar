# Consultas de validação

# Consulta para identificar total de vendas por mês
SELECT
    TO_CHAR(data_pedido, 'YYYY-MM') AS mes,
    SUM(valor_total) AS total_vendas
FROM pedidos
GROUP BY TO_CHAR(data_pedido, 'YYYY-MM')
ORDER BY mes;

# Consulta para identificar quantidade de pedidos por estado
SELECT
    c.estado,
    COUNT(p.id) AS total_pedidos
FROM pedidos p
JOIN clientes c ON p.cliente_id = c.id
GROUP BY c.estado
ORDER BY total_pedidos DESC;

# Consulta para identificar pedidos divergentes
SELECT
    id,
    valor_total,
    valor_itens,
    ABS(valor_total - valor_itens) AS diferenca
FROM pedidos
WHERE divergente = TRUE
ORDER BY diferenca DESC;