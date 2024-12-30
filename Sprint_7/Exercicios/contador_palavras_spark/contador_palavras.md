# Exercício contardor de palavras com Spark

## Objetivo

Desenvolver um job de processamento com o framework Spark por meio de um container Docker.

## Etapa 1 

Realizando o pull da imagem jupyter/all-spark-notebook

![pull_imagem](/Sprint_7/Evidencias/contador_palavras/pull_imagem.png)

## Etapa 2

Executar o container e entrar no link que dará acesso ao Jupyter Lab

![container_exec](/Sprint_7/Evidencias/contador_palavras/container_exec.png)

## Etapa 3 

Executar pyspark e utilizando wget dentro do spark fazer a download do README.md do repositório.

![pyspark](/Sprint_7/Evidencias/contador_palavras/pyspark_1.png)

![readme_carregado](/Sprint_7/Evidencias/contador_palavras/readme_carregado.png)

![readme_salvo](/Sprint_7/Evidencias/contador_palavras/readme_salvo.png) 

## Etapa 4 

Executar sequencia de comando para realizar a contagem de palavras no README.md e gerar um arquivo csv com dados da contagem.

![contador_1](/Sprint_7/Evidencias/contador_palavras/contador-1.png)
![contador_2](/Sprint_7/Evidencias/contador_palavras/contador-2.png)
![contador_3](/Sprint_7/Evidencias/contador_palavras/contador-3.png)
![contador_4](/Sprint_7/Evidencias/contador_palavras/contador-4.png)

Arquivo csv [word_counts_final](/Sprint_7/Exercicios/word_counts_final.csv) com a contagem de palavras do README.md
