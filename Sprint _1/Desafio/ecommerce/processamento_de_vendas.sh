#!/bin/bash

############################################
#
# processamento_de_vendas.sh
#
# Autor: Elivélton Neves de Alcântara (neves_elivelton@yahoo.com.br)
# Data de Criação: 27/09/2024
#
# Descrição: Essse script processa e gera relatórios de vendas, retornando informções
# data da primeira e ultima venda, quantidade total de itens diferentes vendidos e as
# 10 primeiras linhas do arquivo de dados de vendas.
#
# Exemplo de uso: ./processamento de vendas.sh
#
#############################################

cd home/elivelton/Documentos/ecommerce

# Criar diretório vendas
mkdir -p vendas

# Copiar dados de vendas para a pasta vendas
cp dados_de_vendas.csv vendas/

# Criar diretório backup dentro de vendas
cd vendas
mkdir -p backup

# Copiar o arquivo de vendas para o diretório backup e alterar o nome com a data de execução (dados-YYYYMMDD.csv)
cp dados_de_vendas.csv backup/dados-$(date +"%Y%m%d").csv

# Ir para a pasta backup
cd backup

# Renomear o arquivo dentro da pasta backup
mv dados-$(date +"%Y%m%d").csv backup-dados-$(date +"%Y%m%d").csv

# Variável que cria o nome do relatório com data e hora do processamento
relatorio="relatorio$(date +"%Y%m%d").txt"

# Criar arquivo de relatório com as informações de vendas e sistema
echo "Data do Sistema Operacional: $(date +"%Y/%m/%d %H:%M")" > "$relatorio"
echo "Data do Primeiro Registro de Venda: $(head -n 2 backup-dados-$(date +"%Y%m%d").csv | tail -n 1 | cut -d',' -f5)" >> "$relatorio"
echo "Data do Último Registro de Venda: $(tail -n 1 backup-dados-$(date +"%Y%m%d").csv | cut -d',' -f5)" >> "$relatorio"
echo "Total de itens vendidos: $(cut -d',' -f2 backup-dados-$(date +"%Y%m%d").csv | tail -n +2 | sort | uniq | wc -l)" >> "$relatorio"
echo "Primeiras 10 linhas do arquivo backup-dados:" >> "$relatorio"
head -n 10 backup-dados-$(date +"%Y%m%d").csv >> "$relatorio"

# Comprimir o arquivo backup-dados
zip backup-dados-$(date +"%Y%m%d").zip backup-dados-$(date +"%Y%m%d").csv

# Apagar o arquivo original backup-dados.csv e dados-de-vendas.csv
rm backup-dados-$(date +"%Y%m%d").csv
rm ../dados_de_vendas.csv

