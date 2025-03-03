SELECT
    livro.cod AS CodLivro,
    livro.titulo AS Titulo,
    livro.autor as CodAutor,
    autor.nome AS NomeAutor,
    livro.Valor as Valor,
    editora.codeditora AS CodEditora,
    editora.nome AS NomeEditora

FROM
    livro

LEFT JOIN
    autor ON livro.autor = autor.codautor
LEFT JOIN
    editora ON livro.editora = editora.codeditora

ORDER BY
    livro.valor DESC
    
LIMIT 10