select
    editora.codeditora as CodEditora,
    editora.nome as NomeEditora,
    count(*) as QuantidadeLivros

from
    livro
join
    editora on livro.editora = editora.codeditora
group by
    editora.nome

order by
    quantidadelivros desc

limit 5;