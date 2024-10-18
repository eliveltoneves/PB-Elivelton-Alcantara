SELECT 
	dependente.cddep,
    dependente.nmdep,
    dependente.dtnasc,
    SUM(vendas.qtd * vendas.vrunt) as valor_total_vendas

FROM
	tbdependente as dependente
    
JOIN 
	tbvendedor as vendedor
    on dependente.cdvdd = vendedor.cdvdd
JOIN
	tbvendas as vendas
    on vendedor.cdvdd = vendas.cdvdd
    
 WHERE 
 	vendas.status = 'Concluído'
    
GROUP BY 
	dependente.cddep

ORDER BY 
	valor_total_vendas ASC
    
LIMIT 1