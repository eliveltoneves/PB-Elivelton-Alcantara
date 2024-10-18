SELECT 
    vendas.cdven
FROM 
    tbvendas AS vendas
WHERE 
    vendas.deletado = '1'
ORDER BY 
    vendas.cdven ASC;