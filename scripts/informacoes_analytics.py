from scripts.metricas_analytics import carregar_metricas_analytics, dimensoes_analytics
from scripts.visualizacoes import criar_tabela

import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def criar_filtros_analytics(dimensoes_disponiveis):
    """Cria um filtro na sidebar para selecionar um mês e obter o primeiro e último dia do período."""

    with st.sidebar:
        with st.expander('Analytics', expanded=False):
            data_hoje = datetime.today()
            data_min = datetime(2023, 5, 1)

            # Criar lista de datas de início e fim do mês
            datas_inicio = pd.date_range(start=data_min, end=data_hoje, freq='MS')  # MS = início do mês
            datas_fim = [data + relativedelta(day=31) for data in datas_inicio]  # Último dia do mês

            # Formatar datas como string (DD/MM/YYYY)
            datas_inicio_fmt = [data.strftime('%d/%m/%Y') for data in datas_inicio]
            datas_fim_fmt = [data.strftime('%d/%m/%Y') for data in datas_fim]

            col_data_inicio, col_data_fim = st.columns(2)

            # Criar selectboxes para selecionar início e fim do período
            data_inicio = col_data_inicio.selectbox(
                "Início do período",
                datas_inicio_fmt,
                index=0
            )

            data_fim = col_data_fim.selectbox(
                "Fim do período",
                datas_fim_fmt,
                index=len(datas_fim_fmt) - 1
            )

            if pd.to_datetime(data_fim) < pd.to_datetime(data_inicio):
                st.error(
                    "A data de início não pode ser posterior à data de fim. Selecione um período válido.")
                st.stop()  # Interrompe a execução do código

            # Escolher dimensão
            dimensao_selecionada = st.selectbox(
                "Escolha uma dimensão:",
                list(dimensoes_disponiveis.keys()),
                format_func=lambda x: dimensoes_disponiveis[x]
            )

    return data_fim, data_inicio, dimensao_selecionada


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

    data_fim, data_inicio, dimensao_selecionada = criar_filtros_analytics(dimensoes_disponiveis)

    st.header("Informações do Analytics")

    df_analytics, df_analytics_deltas, data_inicio_anterior, data_fim_anterior = carregar_metricas_analytics(
        data_anterior=str(data_inicio),
        data_atual=str(data_fim))

    exibir_kpis_analytics(df_analytics, df_analytics_deltas)

    # Exibir informações desagregadas
    st.subheader("Informações Desagregadas")

    df_dim = dimensoes_analytics(dimensao=[dimensao_selecionada], data_anterior=data_inicio, data_atual=data_fim)

    criar_tabela(df_dim, dimensao_selecionada, dimensoes_disponiveis[dimensao_selecionada], True)

    return df_analytics, df_analytics_deltas, data_fim, data_inicio, data_inicio_anterior, data_fim_anterior
