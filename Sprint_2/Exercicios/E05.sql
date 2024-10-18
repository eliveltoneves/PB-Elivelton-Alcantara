SELECT DISTINCT 
	autor.nome
FROM autor

JOIN livro on autor.codautor = livro.autor

JOIN editora on livro.editora = editora.codeditora

JOIN endereco on endereco.codendereco = editora.endereco

WHERE endereco.estado NOT IN('RIO GRANDE DO SUL', 'PARANÁ')

ORDER BY autor.nome ASC


-- editoras da regiao sul PARANÁ, RIO GRANDE DO SUL