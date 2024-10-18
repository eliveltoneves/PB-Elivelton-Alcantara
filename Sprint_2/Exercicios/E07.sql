SELECT autor.nome

FROM autor

LEFT JOIN LIVRO
	ON autor.codAutor = livro.autor
    
GROUP BY autor.codAutor

HAVING COUNT(livro.cod) = 0

ORDER BY autor.nome ASC;
