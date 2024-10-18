SELECT 
	vendas.estado,
    ROUND(AVG(vendas.qtd * vendas.vrunt), 2) as gastomedio

FROM 
	tbvendas as vendas

WHERE 
	vendas.status = 'Concluído'
    
GROUP BY
	vendas.estado
    
ORDER BY
	gastomedio DESC
