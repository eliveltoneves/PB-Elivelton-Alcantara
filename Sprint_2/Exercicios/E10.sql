SELECT
    vendedor.nmvdd AS vendedor,
    SUM(vendas.qtd * vendas.vrunt) AS valor_total_vendas,
    ROUND((SUM(vendas.qtd * vendas.vrunt) * vendedor.perccomissao / 100), 2) AS comissao
FROM
    tbvendas AS vendas
JOIN 
    tbvendedor AS vendedor 
    ON vendas.cdvdd = vendedor.cdvdd
WHERE 
    vendas.status = 'Concluído'
GROUP BY 
    vendedor.nmvdd, vendedor.perccomissao
ORDER BY 
    comissao DESC;