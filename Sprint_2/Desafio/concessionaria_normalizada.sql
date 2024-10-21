CREATE TABLE Cliente (
    idCliente INT PRIMARY KEY,
    nomeCliente VARCHAR(100),
    cidadeCliente VARCHAR(40),
    estadoCliente VARCHAR(40),
    paisCliente VARCHAR(40)
);

-- Tabela Carro
CREATE TABLE Carro (
    idCarro INT PRIMARY KEY,
    kmCarro INT,
    classiCarro VARCHAR(50),
    marcaCarro VARCHAR(80),
    modeloCarro VARCHAR(80),
    anoCarro INT
);

-- Tabela Combustível
CREATE TABLE Combustivel (
    idCombustivel INT PRIMARY KEY,
    tipoCombustivel VARCHAR(20)
);

-- Tabela Vendedor
CREATE TABLE Vendedor (
    idVendedor INT PRIMARY KEY,
    nomeVendedor VARCHAR(15),
    sexoVendedor SMALLINT,
    estadoVendedor VARCHAR(40)
);


-- Tabela Locação
CREATE TABLE Locacao (
    idLocacao INT PRIMARY KEY,
    idCliente INT,
    idCarro INT,
    idCombustivel INT,
    idVendedor INT,
    dataLocacao DATETIME,
    horaLocacao TIME,
    qtdDiaria INT,
    vlrDiaria DECIMAL(18, 2),
    dataEntrega DATE,
    horaEntrega TIME,
    FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente),
    FOREIGN KEY (idCarro) REFERENCES Carro(idCarro),
    FOREIGN KEY (idCombustivel) REFERENCES Combustivel(idCombustivel),
    FOREIGN KEY (idVendedor) REFERENCES Vendedor(idVendedor)
);

-- Inserir dados na tabela Cliente
INSERT OR IGNORE INTO Cliente (idCliente, nomeCliente, cidadeCliente, estadoCliente, paisCliente)
SELECT DISTINCT idCliente, nomeCliente, cidadeCliente, estadoCliente, paisCliente
FROM tb_locacao;

-- Inserir dados na tabela Carro
INSERT OR IGNORE INTO Carro (idCarro, kmCarro, classiCarro, marcaCarro, modeloCarro, anoCarro)
SELECT DISTINCT idCarro, kmCarro, classiCarro, marcaCarro, modeloCarro, anoCarro
FROM tb_locacao;

-- Inserir dados na tabela Combustivel
INSERT OR IGNORE INTO Combustivel (idCombustivel, tipoCombustivel)
SELECT DISTINCT idCombustivel, tipoCombustivel
FROM tb_locacao;

-- Inserir dados na tabela Vendedor
INSERT OR IGNORE INTO Vendedor (idVendedor, nomeVendedor, sexoVendedor, estadoVendedor)
SELECT DISTINCT idVendedor, nomeVendedor, sexoVendedor, estadoVendedor
FROM tb_locacao;

-- Inserir dados na tabela Locacao, com as correções de data e hora
INSERT OR IGNORE INTO Locacao (idLocacao, idCliente, idCarro, idCombustivel, idVendedor, dataLocacao, horaLocacao, qtdDiaria, vlrDiaria, dataEntrega, horaEntrega)
SELECT idLocacao, idCliente, idCarro, idCombustivel, idVendedor,
       -- Corrigir formato da data de locação
       SUBSTR(dataLocacao, 1, 4) || '-' || SUBSTR(dataLocacao, 5, 2) || '-' || SUBSTR(dataLocacao, 7, 2) AS dataLocacao,

       -- Corrigir horaLocacao, adicionando zero à esquerda se necessário
       CASE 
           WHEN LENGTH(horaLocacao) = 4 THEN '0' || horaLocacao
           ELSE horaLocacao
       END AS horaLocacao,

       qtdDiaria, vlrDiaria,

       -- Corrigir formato da data de entrega
       SUBSTR(dataEntrega, 1, 4) || '-' || SUBSTR(dataEntrega, 5, 2) || '-' || SUBSTR(dataEntrega, 7, 2) AS dataEntrega,

       -- Corrigir horaEntrega, adicionando zero à esquerda se necessário
       CASE 
           WHEN LENGTH(horaEntrega) = 4 THEN '0' || horaEntrega
           ELSE horaEntrega
       END AS horaEntrega
FROM tb_locacao;

sELECT * FROM Cliente

SELECT * FROM Carro

SELECT * FROM Combustivel

SELECT * FROM Vendedor

SELECT * FROM Locacao