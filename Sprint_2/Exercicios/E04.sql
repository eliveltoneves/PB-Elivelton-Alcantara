SELECT 
    autor.nome,
    autor.codautor,
    autor.nascimento,
    COUNT(livro.cod) as quantidade
FROM autor

LEFT JOIN livro 
    on autor.codautor = livro.autor

GROUP BY autor.codautor

ORDER BY autor.nome
