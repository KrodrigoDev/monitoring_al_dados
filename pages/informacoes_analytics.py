import streamlit as st
import pandas as pd
from scripts.metricas_analytics import carregar_metricas_analytics, dimensoes_analytics


def criar_filtros_analytics(df: pd.DataFrame):
    """Cria os filtros na sidebar."""

    with st.sidebar:
        st.subheader('Filtros')

        with st.expander('Analytics', expanded=True):
            datas_unicas = df['data_coleta'].unique().tolist()

            col_data_atual, col_data_anterior = st.columns(2)
            data_atual = col_data_atual.selectbox('Data Atual', datas_unicas, index=len(datas_unicas) - 1)
            data_anterior = col_data_anterior.selectbox('Data Anterior', datas_unicas, index=0)

            # Validar se a data atual é maior ou igual à data anterior
            if pd.to_datetime(data_atual) < pd.to_datetime(data_anterior):
                st.error("A data atual não pode ser menor que a data anterior. Por favor, selecione datas válidas.")
                st.stop()  # Interrompe a execução do código

    return data_atual, data_anterior


def exibir_kpis_analytics(df_analytics, df_analytics_deltas):
    """Exibe os KPIs do Google Analytics."""
    col_1, col_2, col_3, col_4 = st.columns(4)

    col_1.metric("Usuários Ativos", int(df_analytics["Usuários Ativos"][0]),
                 int(df_analytics_deltas["Usuários Ativos"][0]))
    col_2.metric("Novos Usuários", int(df_analytics["Novos Usuários"][0]),
                 int(df_analytics_deltas["Novos Usuários"][0]))
    col_3.metric("Sessões", int(df_analytics["Sessões"][0]), int(df_analytics_deltas["Sessões"][0]))
    col_4.metric("Sessões Engajadas", int(df_analytics["Sessões Engajadas"][0]),
                 int(df_analytics_deltas["Sessões Engajadas"][0]))

    col_5, col_6, col_7 = st.columns(3)
    col_5.metric("Taxa de Engajamento", round(float(df_analytics["Taxa de Engajamento"][0]), 2),
                 round(float(df_analytics_deltas["Taxa de Engajamento"][0]), 2))
    col_6.metric("Páginas Visualizadas", int(df_analytics["Páginas Visualizadas"][0]),
                 int(df_analytics_deltas["Páginas Visualizadas"][0]))
    col_7.metric("Eventos", int(df_analytics["Eventos"][0]), int(df_analytics_deltas["Eventos"][0]))


def exibir_tabela_desagregada(dimensao_selecionada, dimensoes_disponiveis, data_anterior, data_atual):
    """Exibe a tabela desagregada de acordo com a dimensão selecionada."""
    df_dim = dimensoes_analytics(dimensao=[dimensao_selecionada], data_anterior=data_anterior, data_atual=data_atual)
    visualizacoes.criar_tabela(df_dim, dimensao_selecionada, dimensoes_disponiveis[dimensao_selecionada], True)


# --- Fluxo Principal ---
def main():
    # Exibir KPIs do Analytics
    st.header("Informações do Analytics")
    st.subheader("Visão Geral")
    df_analytics, df_analytics_deltas = carregar_metricas_analytics(data_anterior=str(data_anterior),
                                                                    data_atual=str(data_atual))
    exibir_kpis_analytics(df_analytics, df_analytics_deltas)

    # Exibir informações desagregadas
    st.subheader("Informações Desagregadas")
    dimensoes_disponiveis = {
        'country': 'País',
        'region': 'Região',
        'city': 'Cidade',
        'pagePath': 'Páginas visitadas',
        'deviceCategory': 'Categoria do dispositivo',
        'browser': 'Navegador',
        'operatingSystem': 'Sistema Operacional',
        'sessionSource': 'Fonte da sessão',
        'pageTitle': 'Título da Página',
    }
    dimensao_selecionada = st.selectbox("Escolha uma dimensão:", list(dimensoes_disponiveis.keys()),
                                        format_func=lambda x: dimensoes_disponiveis[x])
    exibir_tabela_desagregada(dimensao_selecionada, dimensoes_disponiveis, data_anterior, data_atual)

    # Gerar resumo geral
    st.header("Resumo Geral")
    gemini_ia.gerar_resumo_e_pdf(
        gemini_ia=gemini_ia,
        df_ckan={
            "Total de Organizações": df_atual['nome_organizacao'].nunique(),
            "Organizações com pacotes": df_atual[df_atual['qtd_recurso_pacote'] > 0]['nome_organizacao'].nunique(),
            "Total de pacotes": df_atual['nome_pacote'].nunique(),
            "Total de recursos": df_atual['qtd_recurso_pacote'].sum(),
        },
        df_analytics={
            "Usuários Ativos": df_analytics["Usuários Ativos"][0],
            "Novos Usuários": df_analytics["Novos Usuários"][0],
            "Sessões": df_analytics["Sessões"][0],
            "Sessões Engajadas": df_analytics["Sessões Engajadas"][0],
            "Taxa de Engajamento": df_analytics["Taxa de Engajamento"][0],
            "Páginas Visualizadas": df_analytics["Páginas Visualizadas"][0],
            "Eventos": df_analytics["Eventos"][0],
        },
        df_deltas={
            "delta_orgs": df_atual['nome_organizacao'].nunique() - df_anterior['nome_organizacao'].nunique(),
            "delta_pacotes": df_atual['nome_pacote'].nunique() - df_anterior['nome_pacote'].nunique(),
            "delta_recursos": df_atual['qtd_recurso_pacote'].sum() - df_anterior['qtd_recurso_pacote'].sum(),
            "delta_usuarios_ativos": df_analytics_deltas["Usuários Ativos"][0],
            "delta_sessoes": df_analytics_deltas["Sessões"][0],
            "delta_taxa_engajamento": df_analytics_deltas["Taxa de Engajamento"][0],
            "delta_paginas_visualizadas": df_analytics_deltas["Páginas Visualizadas"][0],
        },
        data_atual=data_atual,
        data_anterior=data_anterior
    )
