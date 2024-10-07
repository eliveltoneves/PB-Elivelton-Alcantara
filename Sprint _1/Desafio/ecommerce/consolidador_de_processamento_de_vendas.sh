#!/bin/bash

############################################
#
#consolidador_de_ processamento_de_vendas.sh
#
# Autor: Elivélton Neves de Alcântara (neves_elivelton@yahoo.com.br)
# Data de Criação: 01/10/2024
#
# Descrição: Essse script processao os relatórios de vendas diários, retornando
# retornado um aquivo chamado relatório_final.txt que une todos os relatórios gerados
#
# Exemplo de uso: ./processamento de vendas.sh
#
#############################################

# Caminho para o diretório de backup onde estão os relatórios
backup_dir="/home/elivelton/Documentos/ecommerce/vendas/backup"

# Nome do arquivo final de relatório
relatorio_final="relatorio_final.txt"

# Criar o arquivo de relatório final
echo "Relatório Consolidado de Vendas" > "$backup_dir/$relatorio_final"
echo "========================================" >> "$backup_dir/$relatorio_final"
echo "Data do Sistema Operacional: $(date +"%Y/%m/%d %H:%M")" >> "$backup_dir/$relatorio_final"
echo "========================================" >> "$backup_dir/$relatorio_final"
echo "" >> "$backup_dir/$relatorio_final"

# Função para consolidar o conteúdo de um relatório específico
consolidar_relatorio() {
    local arquivo=$1

    # Nome do relatório em formato legível
    nome_relatorio=$(basename "$arquivo" | sed 's/relatorio//g' | sed 's/.txt//g')

    echo "Relatório de Vendas - Data: $nome_relatorio" >> "$backup_dir/$relatorio_final"
    echo "----------------------------------------" >> "$backup_dir/$relatorio_final"
    
    # Adicionar o conteúdo do relatório ao arquivo final
    cat "$arquivo" >> "$backup_dir/$relatorio_final"
    
    echo "" >> "$backup_dir/$relatorio_final"
    echo "========================================" >> "$backup_dir/$relatorio_final"
    echo "" >> "$backup_dir/$relatorio_final"
}

# Listar os arquivos de backup na pasta (relatorios .txt que começam com "relatorio")
for arquivo in "$backup_dir"/relatorio*.txt; do
    if [[ "$arquivo" != *"$relatorio_final"* ]]; then
        consolidar_relatorio "$arquivo"
    fi
done

# Mensagem final
echo "Relatório consolidado foi gerado com sucesso em $backup_dir/$relatorio_final."



