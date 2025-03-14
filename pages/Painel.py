import streamlit as st
from scripts.informacoes_analytics import fluxo_analytics
from scripts.infomacoes_ckan import fluxo_ckan
import scripts.gemini_ia as gemini_ia
from scripts.configuracoes_gerais import config_pagina

config_pagina('Visão Geral')

tab1, tab2 = st.tabs(["Ckan", "Analytics"])

with tab1:
    df_atual, df_anterior, data_atual_ckan, data_anterior_ckan = fluxo_ckan()
with tab2:
    df_analytics, df_analytics_deltas, data_atual_analytics, data_anterior_analytics, data_inicio_anterior, data_fim_anterior = fluxo_analytics()

# Gerar resumo geral
with st.sidebar:
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
        data_atual_ckan=data_atual_ckan,
        data_anterior_ckan=data_anterior_ckan,
        data_atual_analytics=data_atual_analytics,
        data_anterior_analytics=data_anterior_analytics,
        data_inicio_anterior=data_inicio_anterior,
        data_fim_anterior=data_fim_anterior
    )
