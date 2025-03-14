import streamlit as st
import pandas as pd
from datetime import datetime
from scripts.metricas_analytics import carregar_metricas_analytics, dimensoes_analytics
from scripts.visualizacoes import criar_tabela


def criar_filtros_analytics(dimensoes_disponiveis):
    """Cria os filtros na sidebar com datas organizadas por mês desde janeiro até a data atual."""
    with st.sidebar:
        with st.expander('Analytics', expanded=False):
            # Definir a data inicial como janeiro do ano atual
            data_atual = datetime.today()
            data_min = datetime(2023, 1, 1)

            # Criar a lista de datas por mês desde janeiro até o mês atual
            datas_mensais = pd.date_range(start=data_min, end=data_atual, freq='ME').strftime('%d/%m/%Y').tolist()

            col_data_atual, col_data_anterior = st.columns(2)
            data_atual = col_data_atual.selectbox('Data Atual', datas_mensais, index=len(datas_mensais) - 1)
            data_anterior = col_data_anterior.selectbox('Data Anterior', datas_mensais, index=len(datas_mensais) - 2)

            # Validar se a data atual é maior ou igual à data anterior
            if pd.to_datetime(data_atual, dayfirst=True) < pd.to_datetime(data_anterior, dayfirst=True):
                st.error("A data atual não pode ser menor que a data anterior. Por favor, selecione datas válidas.")
                st.stop()  # Interrompe a execução do código

            dimensao_selecionada = st.selectbox("Escolha uma dimensão:", list(dimensoes_disponiveis.keys()),
                                                format_func=lambda x: dimensoes_disponiveis[x])

    return data_atual, data_anterior, dimensao_selecionada


def exibir_kpis_analytics(df_analytics, df_analytics_deltas):
    """Exibe os KPIs do Google Analytics."""
    col_1, col_2, col_3, col_4 = st.columns(4)

    col_1.container(border=True).metric("Usuários Ativos", int(df_analytics["Usuários Ativos"][0]),
                                        int(df_analytics_deltas["Usuários Ativos"][0]))
    col_2.container(border=True).metric("Novos Usuários", int(df_analytics["Novos Usuários"][0]),
                                        int(df_analytics_deltas["Novos Usuários"][0]))
    col_3.container(border=True).metric("Sessões", int(df_analytics["Sessões"][0]),
                                        int(df_analytics_deltas["Sessões"][0]))
    col_4.container(border=True).metric("Sessões Engajadas", int(df_analytics["Sessões Engajadas"][0]),
                                        int(df_analytics_deltas["Sessões Engajadas"][0]))

    col_5, col_6, col_7 = st.columns(3)
    col_5.container(border=True).metric("Taxa de Engajamento", round(float(df_analytics["Taxa de Engajamento"][0]), 2),
                                        round(float(df_analytics_deltas["Taxa de Engajamento"][0]), 2))
    col_6.container(border=True).metric("Páginas Visualizadas", int(df_analytics["Páginas Visualizadas"][0]),
                                        int(df_analytics_deltas["Páginas Visualizadas"][0]))
    col_7.container(border=True).metric("Eventos", int(df_analytics["Eventos"][0]),
                                        int(df_analytics_deltas["Eventos"][0]))


# --- Fluxo Principal ---
def fluxo_analytics():
    # config_pagina('Visão Geral')

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

    data_atual, data_anterior, dimensao_selecionada = criar_filtros_analytics(dimensoes_disponiveis)

    st.header("Informações do Analytics")

    df_analytics, df_analytics_deltas, data_inicio_anterior, data_fim_anterior = carregar_metricas_analytics(
        data_anterior=str(data_anterior),
        data_atual=str(data_atual))

    exibir_kpis_analytics(df_analytics, df_analytics_deltas)

    # Exibir informações desagregadas
    st.subheader("Informações Desagregadas")

    df_dim = dimensoes_analytics(dimensao=[dimensao_selecionada], data_anterior=data_anterior, data_atual=data_atual)

    criar_tabela(df_dim, dimensao_selecionada, dimensoes_disponiveis[dimensao_selecionada], True)

    return df_analytics, df_analytics_deltas, data_atual, data_anterior, data_inicio_anterior, data_fim_anterior
