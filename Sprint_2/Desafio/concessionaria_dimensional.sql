-- Dimensão de Cliente
CREATE VIEW dim_cliente AS
SELECT 
    idCliente AS cliente_key,
    nomeCliente,
    cidadeCliente,
    estadoCliente,
    paisCliente
FROM Cliente;

-- Dimensão de Carro
CREATE VIEW dim_carro AS
SELECT 
    idCarro AS carro_key,
    kmCarro,
    classiCarro,
    marcaCarro,
    modeloCarro,
    anoCarro
FROM Carro;

-- Dimensão de Vendedor
CREATE VIEW dim_vendedor AS
SELECT 
    idVendedor AS vendedor_key,
    nomeVendedor,
    sexoVendedor,
    estadoVendedor
FROM Vendedor;

-- Dimensão de Combustível
CREATE VIEW dim_combustivel AS
SELECT 
    idCombustivel AS combustivel_key,
    tipoCombustivel
FROM Combustivel;

-- Dimensão de Tempo (baseada nas datas de locação e entrega)
CREATE VIEW dim_tempo AS
SELECT DISTINCT
    dataLocacao AS data_key,
    strftime('%Y', dataLocacao) AS ano,
    strftime('%m', dataLocacao) AS mes,
    strftime('%d', dataLocacao) AS dia,
    CASE
        WHEN strftime('%w', dataLocacao) = '0' THEN 'Domingo'
        WHEN strftime('%w', dataLocacao) = '1' THEN 'Segunda-feira'
        WHEN strftime('%w', dataLocacao) = '2' THEN 'Terça-feira'
        WHEN strftime('%w', dataLocacao) = '3' THEN 'Quarta-feira'
        WHEN strftime('%w', dataLocacao) = '4' THEN 'Quinta-feira'
        WHEN strftime('%w', dataLocacao) = '5' THEN 'Sexta-feira'
        WHEN strftime('%w', dataLocacao) = '6' THEN 'Sábado'
    END AS dia_semana,
    strftime('%m', dataLocacao) AS mes_numero,
    CASE 
        WHEN strftime('%m', dataLocacao) = '01' THEN 'Janeiro'
        WHEN strftime('%m', dataLocacao) = '02' THEN 'Fevereiro'
        WHEN strftime('%m', dataLocacao) = '03' THEN 'Março'
        WHEN strftime('%m', dataLocacao) = '04' THEN 'Abril'
        WHEN strftime('%m', dataLocacao) = '05' THEN 'Maio'
        WHEN strftime('%m', dataLocacao) = '06' THEN 'Junho'
        WHEN strftime('%m', dataLocacao) = '07' THEN 'Julho'
        WHEN strftime('%m', dataLocacao) = '08' THEN 'Agosto'
        WHEN strftime('%m', dataLocacao) = '09' THEN 'Setembro'
        WHEN strftime('%m', dataLocacao) = '10' THEN 'Outubro'
        WHEN strftime('%m', dataLocacao) = '11' THEN 'Novembro'
        WHEN strftime('%m', dataLocacao) = '12' THEN 'Dezembro'
    END AS mes_nome
FROM Locacao;

--Fato Locacao
CREATE VIEW fato_locacao AS
SELECT 
    L.idLocacao AS locacao_key,
    C.idCliente AS cliente_key,
    A.idCarro AS carro_key,
    V.idVendedor AS vendedor_key,
    B.idCombustivel AS combustivel_key,
    L.qtdDiaria,
    L.vlrDiaria,
    L.dataLocacao AS data_locacao_key,
    L.dataEntrega AS data_entrega_key,
    -- Métrica calculada (valor total da locação)
    (L.qtdDiaria * L.vlrDiaria) AS valor_total_locacao,
    -- Métrica calculada (duração da locação (em dias))
    JULIANDAY(L.dataEntrega) - JULIANDAY(L.dataLocacao) AS duracao_locacao
FROM Locacao L
JOIN Cliente C ON L.idCliente = C.idCliente
JOIN Carro A ON L.idCarro = A.idCarro
JOIN Vendedor V ON L.idVendedor = V.idVendedor
JOIN Combustivel B ON L.idCombustivel = B.idCombustivel;