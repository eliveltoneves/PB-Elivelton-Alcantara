# Documentação do Projeto: Análise de Dados de Aplicativos do Google Play Store

## Descrição Geral

Este projeto tem como objetivo explorar e analisar dados de aplicativos da Google Play Store. Realizamos uma série de análises para identificar tendências, padrões e insights sobre os aplicativos. A análise é baseada no dataset googleplaystore.csv, e os resultados são apresentados em gráficos e estatísticas que facilitam a compreensão dos dados.

## Estrutura do Projeto

### 1 - Importando Bibliotecas e Lendo o Dataset

 Nesta etapa inicial, foram importadas as bibliotecas Pandas e Matplotlib, essenciais para manipulação de dados e visualização. Em seguida, carregamos o dataset googleplaystore.csv, aplicando um processamento inicial para remover duplicatas. A remoção de linhas duplicadas garante a consistência dos dados, eliminando entradas que poderiam distorcer nossas análises.

 ![importando_dataset](/Sprint_3/Evidencias/importando_dataset.png)

### 2 - Gráfico de Barras dos Top 5 Apps por Número de Instalações

 Identificamos os cinco aplicativos com o maior número de instalações e visualizamos esses dados em um gráfico de barras. Esse gráfico facilita a identificação dos aplicativos mais populares em termos de instalações, fornecendo uma visão sobre quais aplicativos possuem a maior base de usuários e destacando as preferências dos consumidores.

 ```python
 # Tratando a coluna 'Installs' para converter em valores numéricos
df['Installs'] = pd.to_numeric(df['Installs'].astype(str).str.replace(',', '').str.replace('+', ''), errors='coerce')
df = df.dropna(subset=['Installs'])  # Removendo linhas onde 'Installs' é NaN

# Selecionando os top 5 apps por número de instalações
top_5_installs = df.nlargest(5, 'Installs')[['App', 'Installs']]

# Criando o gráfico de barras para os top 5 aplicativos por número de instalações
plt.figure(figsize=(10, 6))
plt.barh(top_5_installs['App'], top_5_installs['Installs'])
plt.title('Top 5 Apps mais Instalados')
plt.xlabel('Aplicativos')
plt.ylabel('Número de Instalações')
plt.xticks(rotation=45)
plt.show()
```
 ![mais_instalados](/Sprint_3/Evidencias/top_5_mais_instalados.png)

### 3 - Gráfico de Pizza das Categorias de Apps

 Para entender a diversidade e proporção de categorias de aplicativos, criamos um gráfico de pizza que representa a frequência de cada categoria no dataset. Esse gráfico ajuda a visualizar a distribuição das categorias e a proporção que cada uma ocupa no total de aplicativos da loja, permitindo insights sobre áreas com mais presença ou concentração.Para maior legibilidade do gráfico, categorias com 3% ou menos foram agrupadas em outras.

```python
# Calculando a frequência das categorias
category_counts = df['Category'].value_counts()

# Para melhorar a visualização, agrupamos categorias com menos de 3% em "Outros"
threshold = 0.03 * category_counts.sum()  # Calculando o limiar de 3%
small_categories = category_counts[category_counts < threshold]
category_counts = category_counts[category_counts >= threshold]
category_counts['Others'] = small_categories.sum()

# Criar gráfico de pizza
plt.figure(figsize=(10,8))
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors, explode=[0.1 if x == 'Others' else 0 for x in category_counts.index])
plt.title('Distribuição de Categorias de Aplicativos', fontsize=16)
plt.axis('equal')  # Garantir que o gráfico de pizza seja desenhado como um círculo.

# Adicionar legenda para facilitar a leitura
plt.legend(category_counts.index, title="Categorias", bbox_to_anchor=(1.05, 1), loc = 'center')

plt.show()
```
![grafico_pizza](/Sprint_3/Evidencias/grafico_pizza.png)

### 4 -Aplicativo Mais Caro no Dataset

 Nesta etapa, identificamos o aplicativo mais caro disponível no dataset. Esse valor máximo indica a presença de aplicativos premium e o quanto alguns desenvolvedores estão cobrando pelos seus produtos. Essa análise fornece informações sobre a faixa de preços dos aplicativos na loja.

 ![app_mais_caro](/Sprint_3/Evidencias/app_mais_caro.png)

### 5 - Contagem de Apps Classificados como "Mature 17+"

Contamos a quantidade de aplicativos classificados como "Mature 17+", que indicam conteúdo destinado ao público adulto. Esta classificação é relevante para analisar a presença de aplicativos com conteúdo específico, proporcionando um entendimento sobre a quantidade de aplicativos voltados para um público mais maduro.

![mature_17+](/Sprint_3/Evidencias/contage_app_mature17.png)

### 6. Top 10 Apps por Número de Avaliações

Para identificar os aplicativos com maior engajamento dos usuários, listamos os 10 aplicativos com o maior número de avaliações, ordenados em ordem decrescente. Esse ranking ajuda a identificar quais aplicativos têm a maior interação e engajamento do público por meio de avaliações, oferecendo insights sobre os aplicativos mais discutidos e populares na comunidade.

```python
# Convertendo a coluna de Reviews para numérico
df['Reviews'] = df['Reviews'].astype(int)

# Selecionando os top 10 apps por número de avaliações
top_10_reviews = df.nlargest(10, 'Reviews')[['App', 'Reviews']]
top_10_reviews
```

![top_10_mais_avaliados](/Sprint_3/Evidencias/top_10_melhor_avaliados.png)

### 7. Análises Adicionais

Para enriquecer a análise, foram calculadas as seguintes métricas adicionais:

 - Lista da Quantidade de Apps por Faixa Etária: Exibimos a quantidade de aplicativos em cada faixa etária, o que permite entender melhor o direcionamento etário dos aplicativos.

 ![apps_faixaetaria](/Sprint_3/Evidencias/apps_por_faixaetaria.png)

 - Média de Avaliação dos Aplicativos Pagos: Calculamos a média das avaliações dos aplicativos pagos, representada como um único valor numérico. Essa métrica ajuda a entender se os aplicativos pagos estão sendo bem avaliados em comparação com os gratuitos.

 ![media_avaliacao_apps_pagos](/Sprint_3/Evidencias/media_apps_pagos.png)

### 8. Gráficos para os Indicadores

Para uma análise visual mais rica, criamos gráficos adicionais para observar diferentes aspectos dos dados:

- Gráfico de Colunas da Distribuição de Apps por Faixa Etária: Este gráfico apresenta a distribuição dos aplicativos por faixa etária em uma escala logarítmica. A escala logarítmica foi utilizada para permitir a visualização de valores pequenos e grandes, garantindo que todas as categorias estejam visíveis, mesmo aquelas com poucos aplicativos.

```python
# Contar a quantidade de aplicativos para cada faixa etária (Content Rating)
content_rating_counts = df['Content Rating'].value_counts()

# Criar o histograma usando matplotlib
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.bar(content_rating_counts.index, content_rating_counts.values, color='skyblue')
plt.title('Quantidade de Apps por Faixa Etária (Content Rating)', fontsize=16)
plt.xlabel('Faixa Etária (Content Rating)', fontsize=12)
plt.ylabel('Quantidade de Apps', fontsize=12)
plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo x para melhor visualização
plt.yscale('log')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

```

![apps_faixa-etaria](/Sprint_3/Evidencias/qtd_apps_faixaetaria.png)

 - Histograma das Avaliações dos Aplicativos: Criamos um histograma para observar a concentração das avaliações dos aplicativos. Esse gráfico permite visualizar onde a maioria das avaliações está concentrada, revelando a qualidade média e a dispersão das avaliações entre os aplicativos.

 ```python
 # Filtrar os dados para remover valores nulos em 'Rating'
ratings_data = df['Rating'].dropna()

# Criar o histograma
plt.figure(figsize=(10,6))
plt.hist(ratings_data, bins=20, color='skyblue', edgecolor='black')
plt.title('Distribuição das Avaliações dos Apps', fontsize=16)
plt.xlabel('Avaliação (Rating)', fontsize=12)
plt.ylabel('Quantidade de Apps', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show() 
 ```
 ![concentracao_avaliacao](/Sprint_3/Evidencias/concentracao_avaliacoes.png)

 ### Conclusão
 
Este projeto de análise de dados fornece uma visão abrangente sobre os aplicativos disponíveis na Google Play Store, permitindo identificar tendências e preferências dos consumidores. As análises dos preços, das classificações etárias, das categorias mais populares e das avaliações ajudam a entender o cenário competitivo e os interesses dos usuários da loja.

