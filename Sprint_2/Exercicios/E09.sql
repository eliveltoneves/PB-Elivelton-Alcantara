SELECT vendas.cdpro, vendas.nmpro

FROM tbvendas as vendas

WHERE status = 'Concluído' AND
	dtven BETWEEN '2014-02-03' AND '2018-02-02'
    
GROUP BY cdpro

LIMIT 1