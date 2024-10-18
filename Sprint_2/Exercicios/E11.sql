SELECT 
	vendas.cdcli,
    vendas.nmcli,
    SUM(vendas.qtd * vendas.vrunt) AS gasto
    
FROM 
    tbvendas as vendas

WHERE 
    vendas.status = 'Concluído'

GROUP BY 
	vendas.cdcli, vendas.nmcli

ORDER BY gasto DESC

LIMIT 1