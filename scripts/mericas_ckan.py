import pandas as pd
from ckanapi import RemoteCKAN
from dotenv import dotenv_values
import pathlib
import streamlit as st
from datetime import datetime

# Carregar a API key do CKAN
API_KEY_CKAN = dotenv_values('../monitoring_al_dados/data/credenciais.env')['API_KEY_CKAN']

# Conectar à instância CKAN
ckan = RemoteCKAN('https://dados.al.gov.br/catalogo', apikey=API_KEY_CKAN)


def listar_organizacoes(busca_detalhada: bool = True) -> pd.DataFrame:
    """
    Lista as organizações disponíveis no portal CKAN, incluindo métricas detalhadas.

    :param busca_detalhada: Quando True, retorna detalhes completos das organizações.
    :return: DataFrame contendo métricas de organizações e pacotes.
    """
    organizations = ckan.action.organization_list(all_fields=busca_detalhada)
    dfs_pacotes = []

    for organizacao in organizations:
        pacotes_df = listar_pacotes(organizacao['name'])
        if pacotes_df is not None:
            dfs_pacotes.append(pacotes_df)

    df_final = pd.concat(dfs_pacotes, ignore_index=True)
    df_final['nome_organizacao'] = df_final['nome_organizacao'].apply(lambda x: str(x).strip())
    df_final['data_coleta'] = datetime.now().strftime('%d/%m/%Y')

    return df_final


def listar_pacotes(organizacao: str) -> pd.DataFrame:
    """
    Lista os pacotes de uma organização e calcula o total de recursos.

    :param organizacao: Nome da organização no CKAN.
    :return: DataFrame com os pacotes e recursos da organização.
    """
    try:
        pacotes = ckan.action.organization_show(id=organizacao, include_datasets=True)['packages']
        nomes = []
        qtd_recursos = []
        nome_organizacao = []

        if pacotes:
            for pacote in pacotes:
                nomes.append(pacote['title'])
                qtd_recursos.append(pacote['num_resources'])
                nome_organizacao.append(pacote['organization']['title'])
        else:
            nomes.append(None)
            qtd_recursos.append(0)
            nome_organizacao.append(organizacao)

        return pd.DataFrame({
            'nome_pacote': nomes,
            'qtd_recurso_pacote': qtd_recursos,
            'nome_organizacao': nome_organizacao,
        })
    except Exception as e:
        print(f"Erro ao listar os pacotes para a organização {organizacao}: {e}")
        return None


def kpis(df_atual, df_anterior):
    """
    Calcula as métricas e os deltas entre dois períodos de tempo.

    :param df_atual: DataFrame com os dados do período atual.
    :param df_anterior: DataFrame com os dados do período anterior.
    :return: Tupla com as métricas e deltas.
    """

    def calcular_metricas(df):
        return {
            "total_organizacoes": df['nome_organizacao'].nunique(),
            "total_organizacoes_com_dados": df[df['qtd_recurso_pacote'] != 0]['nome_organizacao'].nunique(),
            "total_pacotes": df['nome_pacote'].nunique(),
            "total_recursos": df['qtd_recurso_pacote'].sum()
        }

    atual = calcular_metricas(df_atual)
    anterior = calcular_metricas(df_anterior)

    return (
        atual["total_organizacoes"], atual["total_organizacoes"] - anterior["total_organizacoes"],
        atual["total_pacotes"], atual["total_pacotes"] - anterior["total_pacotes"],
        atual["total_recursos"], atual["total_recursos"] - anterior["total_recursos"],
        atual["total_organizacoes_com_dados"],
        atual["total_organizacoes_com_dados"] - anterior["total_organizacoes_com_dados"]
    )


@st.cache_data
def main_ckan():
    """
    Carrega ou atualiza as métricas do CKAN a partir de um arquivo Excel.
    """
    arquivo = pathlib.Path('../monitoring_al_dados/data/metricas_ckan.xlsx')

    if arquivo.exists():
        df = pd.read_excel(arquivo)
        df = pd.concat([df, listar_organizacoes()], ignore_index=True)
    else:
        df = listar_organizacoes()

    # retirando as duplicatas ( para caso tenha entrado mais de uma vez no dia)
    df = df.drop_duplicates(subset=['data_coleta', 'nome_pacote', 'nome_organizacao'])

    # tratando a coluna de data para seguir o padrão br
    df['data_coleta'] = pd.to_datetime(df['data_coleta'], format='%d/%m/%Y', errors='coerce')
    df['data_coleta'] = df['data_coleta'].dt.strftime('%d/%m/%Y')

    df.dropna(subset='data_coleta', inplace=True)

    df.to_excel(arquivo, index=False)

    return df
