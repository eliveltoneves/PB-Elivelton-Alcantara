SELECT 
	vendas.cdpro,
    vendas.nmcanalvendas,
    vendas.nmpro,
    SUM(vendas.qtd) as quantidade_vendas
    

FROM
	tbvendas as vendas
    
WHERE 
	vendas.status = 'Concluído'
    
GROUP by 
	vendas.cdpro, vendas.nmcanalvendas, vendas.nmpro

ORDER BY
	quantidade_vendas ASC
    
LIMIT 10