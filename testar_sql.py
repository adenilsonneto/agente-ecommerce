from database import executar_sql
import pandas as pd

#ANÁLISE DE VENDAS E RECEITA
sql = """
SELECT p.nome_produto, COUNT(i.id_item) as quantidade_vendida
FROM fat_itens_pedidos i
JOIN dim_produtos p ON i.id_produto = p.id_produto
GROUP BY p.id_produto
ORDER BY quantidade_vendida DESC
LIMIT 10
"""

resultado = executar_sql(sql)
print("Top 10 produtos mais vendidos:\n")
for row in resultado['dados']:
    print(row)

sql = '''SELECT p.categoria_produto, COUNT(DISTINCT i.id_pedido) as total_pedidos, COUNT (i.id_item) as itens_vendidos, ROUND (SUM(i.preco_BRL),2) as receita_total_brl
FROM fat_itens_pedidos i
JOIN dim_produtos p ON i.id_produto = p.id_produto
GROUP BY p.categoria_produto
ORDER BY receita_total_brl DESC'''

resultado = executar_sql(sql)
print("\nReceita total por categoria:\n")
for row in resultado['dados']:
    print(row)

#ANÁLISE DE ENTREGA E LOGISTICA

sql = ''' SELECT status, COUNT(*) as total, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fat_pedidos), 2) as percentual
FROM fat_pedidos
GROUP BY status
ORDER BY total DESC'''

resultado = executar_sql(sql)
print("\nQuantidade de pedidos por status:\n") 
for row in resultado['dados']:
    print(row)

sql = '''SELECT c.estado, COUNT(*) as total_pedidos, SUM(CASE WHEN p.entrega_no_prazo = 'Sim' THEN 1 ELSE 0 END) as no_prazo, ROUND(SUM(CASE WHEN p.entrega_no_prazo = 'Sim' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_no_prazo
FROM fat_pedidos p
JOIN dim_consumidores c ON p.id_consumidor = c.id_consumidor
WHERE p.status = 'entregue'
GROUP BY c.estado
ORDER BY pct_no_prazo DESC'''

resultado = executar_sql(sql)
print("\nDesempenho de entrega por estado em %:\n")
for row in resultado['dados']:
    print(row)

#ANÁLISE DE SATISFAÇÃO E AVALIAÇÕES

sql = '''SELECT ROUND(AVG(avaliacao), 2) as media_geral
FROM fat_avaliacoes_pedidoS '''

resultado = executar_sql(sql)
print("\nMédia de avaliação geral:\n")
for row in resultado['dados']:
    print(row)

sql = '''SELECT v.nome_vendedor, v.estado, COUNT(a.id_avaliacao) as total_avaliacoes, ROUND(AVG(a.avaliacao), 2) as media_avaliacao
FROM fat_avaliacoes_pedidos a
JOIN fat_itens_pedidos i ON a.id_pedido = i.id_pedido
JOIN dim_vendedores v ON i.id_vendedor = v.id_vendedor
GROUP BY v.id_vendedor, v.nome_vendedor, v.estado
HAVING total_avaliacoes >= 10
ORDER BY media_avaliacao DESC
LIMIT 10'''

resultado = executar_sql(sql)
print("\nTop 10 vendedores mais bem avaliados (mínimo 10 avaliações):\n")
for row in resultado['dados']:
    print(row)

#ANÁLISE DE CONSUMIDORES

sql = '''SELECT c.estado, COUNT(DISTINCT pt.id_pedido) as total_pedidos, ROUND(AVG(pt.valor_total_pago_brl), 2) as ticket_medio_brl
FROM fat_pedido_total pt
JOIN dim_consumidores c ON pt.id_consumidor = c.id_consumidor
GROUP BY c.estado
ORDER BY total_pedidos DESC '''

resultado = executar_sql(sql)
print("\nEstados com maior volume de pedidos e ticket médio:\n")
for row in resultado['dados']:
    print(row)

sql = '''SELECT c.estado, COUNT(*) as pedidos_atrasados, ROUND(AVG(p.diferenca_entrega_dias), 1) as atraso_medio_dias
FROM fat_pedidos p
JOIN dim_consumidores c ON p.id_consumidor = c.id_consumidor
WHERE p.entrega_no_prazo = 'Não'
GROUP BY c.estado
ORDER BY atraso_medio_dias DESC
LIMIT 10 '''

resultado = executar_sql(sql) 
print("\nEstados com maior atraso:")
for row in resultado['dados']:
    print(row)

#ANÁLISE DE VENDAS E PRODUTOS

sql = '''SELECT estado, nome_produto, quantidade_vendida
FROM (SELECT c.estado, p.nome_produto, COUNT(i.id_item) as quantidade_vendida, ROW_NUMBER() OVER (PARTITION BY c.estado ORDER BY COUNT(i.id_item) DESC) as ranking
    FROM fat_itens_pedidos i
    JOIN dim_produtos p ON i.id_produto = p.id_produto
    JOIN fat_pedidos fp ON i.id_pedido = fp.id_pedido
    JOIN dim_consumidores c ON fp.id_consumidor = c.id_consumidor
    GROUP BY c.estado, p.id_produto, p.nome_produto
)
WHERE ranking <= 10
ORDER BY estado, quantidade_vendida DESC '''

resultado = executar_sql(sql)
print("\nProdutos mais vendidos por estado:\n")
for row in resultado['dados']:
    print(row)

sql = '''SELECT p.categoria_produto, COUNT(a.id_avaliacao) as total_avaliacoes, SUM(CASE WHEN a.avaliacao <= 2 THEN 1 ELSE 0 END) as avaliacoes_negativas, ROUND(SUM(CASE WHEN a.avaliacao <= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as pct_negativas
FROM fat_avaliacoes_pedidos a
JOIN fat_itens_pedidos i ON a.id_pedido = i.id_pedido
JOIN dim_produtos p ON i.id_produto = p.id_produto
GROUP BY p.categoria_produto
ORDER BY pct_negativas DESC '''

resultado = executar_sql(sql)
print("\nCategorias com maior taxa de avaliações negativas:\n")
for row in resultado['dados']:
    print(row)