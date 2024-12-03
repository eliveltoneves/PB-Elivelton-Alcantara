import pandas as pd
import boto3
from io import StringIO
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError

# Configurações do Bucket S3
BUCKET_NAME = "desafio-sprint-5"  # Nome do bucket existente
INPUT_FILE = "dados_operadoras_s3.csv"  # Nome do arquivo original no S3
PROCESSED_FILE = "dataset_processado.csv"  # Nome do arquivo processado localmente
S3_OBJECT_NAME = "dataset_processado.csv"  # Nome do arquivo processado no S3

def read_file_from_s3(bucket_name, object_name):
    """Ler o arquivo diretamente do S3 e retornar como DataFrame."""
    s3 = boto3.client('s3')
    try:
        print(f"Lendo o arquivo '{object_name}' do bucket '{bucket_name}'...")
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
        csv_string = response['Body'].read().decode('utf-8')
        print(f"Arquivo '{object_name}' lido com sucesso.")
        return pd.read_csv(StringIO(csv_string), sep=";")
    except ClientError as e:
        print(f"Erro ao acessar o arquivo no S3: {e}")
        return None
    except NoCredentialsError:
        print("Credenciais da AWS não configuradas corretamente.")
        return None

def processar_dados(dados):
    """Processar o DataFrame para listar operadoras filtradas e incluir agregações dos estados."""
    print("Processando consultas no DataFrame")

    # Preencher valores ausentes nas colunas importantes
    dados['UF'] = dados['UF'].fillna('Desconhecido')
    dados['Modalidade'] = dados['Modalidade'].fillna('Indefinida')

    # 4.4 - Função de Conversão: Padronização de CEP
    dados['CEP_Padronizado'] = dados['CEP'].apply(lambda x: str(x).zfill(8))

    # 4.5  Cálculo da Idade da Operadora
    dados['Data_Registro_ANS'] = pd.to_datetime(dados['Data_Registro_ANS'], errors='coerce')
    dados['Ano_Registro'] = dados['Data_Registro_ANS'].dt.year
    dados['Idade_Operadora'] = datetime.now().year - dados['Ano_Registro']

    # 4.3 Classificação do Tamanho da Operadora
    def categorizar_tamanho(regioes):
        if regioes <= 2:
            return "Local"
        elif 3 <= regioes <= 5:
            return "Regional"
        else:
            return "Nacional"

    dados['Regiao_de_Comercializacao'] = pd.to_numeric(dados['Regiao_de_Comercializacao'], errors='coerce')
    dados['Tamanho_Operadora'] = dados['Regiao_de_Comercializacao'].apply(categorizar_tamanho)

    # 4.6 Criar coluna Endereço Completo
    dados['CEP_Padronizado'] = dados['CEP'].apply(lambda x: str(x).zfill(8))
    dados['Endereco_Completo'] = (
        dados['Logradouro'].fillna('') + ", " +
        dados['Numero'].fillna('') + ", " +
        dados['Complemento'].fillna('') + ", " +
        dados['Bairro'].fillna('') + ", " +
        dados['Cidade'].fillna('') + ", " +
        dados['UF'] + ", CEP: " +
        dados['CEP_Padronizado']
    )

    # 4.1 Filtro para as operadoras (Razao_Social e demais colunas relacionadas)
    filtro = (
        (dados['UF'] != 'SP') &
        (dados['Modalidade'] == 'Medicina de Grupo') &
        (dados['Idade_Operadora'] >= 15) &
        (dados['Tamanho_Operadora'].isin(['Regional', 'Nacional']))
    )
    operadoras_filtradas = dados[filtro][[
        'Razao_Social',
        'UF',
        'Modalidade',
        'Idade_Operadora',
        'Tamanho_Operadora',
        'CEP_Padronizado',
        'Endereco_Completo'
    ]]

    # 4.2 Agregações para Estados
    estados = sorted(dados['UF'].unique())  # Garantir a ordem alfabética dos estados
    operadoras_por_estado = dados.groupby('UF')['CNPJ'].nunique().reindex(estados, fill_value=0).reset_index(name='Operadoras_Por_Estado')
    modalidades_por_estado = dados.groupby('UF')['Modalidade'].nunique().reindex(estados, fill_value=0).reset_index(name='Modalidades_Por_Estado')

    # Garantir que os valores sejam inteiros
    operadoras_por_estado['Operadoras_Por_Estado'] = operadoras_por_estado['Operadoras_Por_Estado'].astype(int)
    modalidades_por_estado['Modalidades_Por_Estado'] = modalidades_por_estado['Modalidades_Por_Estado'].astype(int)

    # Criar DataFrame com Estados e agregações
    estados_df = pd.DataFrame({'Estado': estados})
    estados_df = estados_df.merge(operadoras_por_estado, how='left', left_on='Estado', right_on='UF').drop(columns=['UF'])
    estados_df = estados_df.merge(modalidades_por_estado, how='left', left_on='Estado', right_on='UF').drop(columns=['UF'])

    # 6. Combinação final (colocar os resultados juntos no mesmo dataset)
    resultado_final = pd.concat(
        [operadoras_filtradas.reset_index(drop=True), estados_df.reset_index(drop=True)],
        axis=1
    )

    # Ajustar a exibição para inteiros sem ponto flutuante
    pd.options.display.float_format = '{:,.0f}'.format

    print("\nNovo DataFrame criado com as colunas organizadas:")
    print(resultado_final.head())

    return resultado_final

def save_to_s3(file_path, bucket_name, object_name):
    """Salvar arquivo local processado de volta ao S3."""
    s3 = boto3.client("s3")
    try:
        print(f"Enviando '{file_path}' para o bucket '{bucket_name}'...")
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"Arquivo enviado com sucesso: s3://{bucket_name}/{object_name}")
        return True
    except FileNotFoundError:
        print(f"Arquivo '{file_path}' não encontrado.")
        return False
    except ClientError as e:
        print(f"Erro ao fazer upload: {e}")
        return False

def main():
    """Executar o processo completo."""
    # Ler arquivo diretamente do S3
    dados = read_file_from_s3(BUCKET_NAME, INPUT_FILE)
    if dados is None:
        print("Falha ao acessar o arquivo no S3. Processo encerrado.")
        return

    # Processar dados
    novo_dataframe = processar_dados(dados)

    # Salvar o DataFrame como CSV localmente
    novo_dataframe.to_csv(PROCESSED_FILE, index=False, encoding="utf-8")
    print(f"Novo DataFrame processado salvo localmente em: {PROCESSED_FILE}")

    # Enviar o arquivo processado para o bucket S3
    if not save_to_s3(PROCESSED_FILE, BUCKET_NAME, S3_OBJECT_NAME):
        print("Falha no upload do arquivo processado para o S3.")
        return

    print("Arquivo processado enviado para o S3 com sucesso!")

if __name__ == "__main__":
    main()
