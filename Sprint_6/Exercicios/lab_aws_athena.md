# Exercício Lab AWS Athena

## Etapa 1

Foi criada uma pasta chamada queries no bucket S3 elivelton.com para armazenar os resultados das consultas. Além disso, o bucket foi configurado como destino para os resultados das consultas no serviço AWS Athena.

![config_caminho_query](/Sprint_6/Evidencias/lab_aws_athena/config_caminho_query.png)

## Etapa 2 

Criado banco de dados no serviço Athena.


![meu_banco](/Sprint_6/Evidencias/lab_aws_athena/meu_banco.png)

### Etapa 3

Criando tabela para o banco de dados.

![Criando_tabela](/Sprint_6/Evidencias/lab_aws_athena/criando_tabela.png)

#### Teste de consulta no banco de dados 

- query para teste:

![query_test](/Sprint_6/Evidencias/lab_aws_athena/query_test.png)

Resultado da query:

![resultado_query_test](/Sprint_6/Evidencias/lab_aws_athena/resultado_query_test.png)

#### Consulta que lista os 3 nomes mais usados em cada década desde o 1950 até hoje.

- query da consulta:

```sql
WITH ranked_names AS (
    SELECT
        nome,
        CAST((ano / 10) * 10 AS INT) AS decada,
        SUM(total) AS total_por_nome,
        RANK() OVER (PARTITION BY CAST((ano / 10) * 10 AS INT) ORDER BY SUM(total) DESC) AS posicao
    FROM meubanco.nomes
    WHERE ano >= 1950
    GROUP BY nome, CAST((ano / 10) * 10 AS INT)
)
SELECT
    decada,
    posicao,
    nome,
    total_por_nome
FROM ranked_names
WHERE posicao <= 3
ORDER BY decada, posicao;
```




Resultado da consulta:

![resultado_consulta](/Sprint_6/Evidencias/lab_aws_athena/resultado_consulta.png)


