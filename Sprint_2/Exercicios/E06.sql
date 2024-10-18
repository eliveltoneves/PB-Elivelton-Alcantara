SELECT 
    autor.codAutor,
    autor.nome,
    COUNT(livro.cod) AS quantidade_publicacoes

FROM AUTOR

JOIN 
    LIVRO  ON autor.codAutor = livro.autor
GROUP BY 
    autor.codAutor, autor.nome
ORDER BY 
    quantidade_publicacoes DESC
LIMIT 1;
