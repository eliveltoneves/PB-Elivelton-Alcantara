select
    vendedor.cdvdd,
    vendedor.nmvdd


from tbvendedor as vendedor

left join tbvendas as vendas
    on vendas.cdvdd = vendedor.cdvdd

where vendas.status = 'Concluído'

order by vendas.status

limit 1
