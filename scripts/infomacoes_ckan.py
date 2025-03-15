import streamlit as st
import pandas as pd
from scripts.mericas_ckan import main_ckan, kpis
from scripts.visualizacoes import criar_tabela


def criar_filtros_ckan(df: pd.DataFrame):
    """Cria os filtros na sidebar."""

    with st.sidebar:
        st.subheader('Filtros')

        with st.expander('Ckan', expanded=False):
            datas_unicas = df['data_coleta'].unique().tolist()

            col_data_anterior, col_data_atual = st.columns(2)
            data_inicio = col_data_anterior.selectbox('Início do período', datas_unicas, index=0)
            data_fim = col_data_atual.selectbox('Fim do período', datas_unicas, index=len(datas_unicas) - 1)

            # Validar se a data atual é maior ou igual à data anterior
            if pd.to_datetime(data_fim) < pd.to_datetime(data_inicio):
                st.error(
                    "A data de início não pode ser posterior à data de fim. Selecione um período válido.")
                st.stop()  # Interrompe a execução do código

            organizacao_selecionada = st.selectbox(
                'Selecionar Organização:', ['Selecionar tudo'] + list(df['nome_organizacao'].unique())
            )

    return data_fim, data_inicio, organizacao_selecionada


def filtrar_dados(df, data_atual, data_anterior, organizacao_selecionada):
    """Filtra os dados conforme as datas e organização selecionadas."""

    if organizacao_selecionada != 'Selecionar tudo':
        df = df[df['nome_organizacao'] == organizacao_selecionada]

    df_atual = df[df['data_coleta'] == data_atual]
    df_anterior = df[df['data_coleta'] == data_anterior]
    return df_atual, df_anterior


def exibir_kpis_ckan(df_atual, df_anterior):
    """Exibe os KPIs do CKAN."""
    (orgs_ultimo_mes, delta_orgs, tot_pacotes_ultimo_mes,
     delta_pacotes, tot_recursos_ultimo_mes, delta_recursos,
     tot_org_dados_ult, delta_org_dados) = kpis(df_atual, df_anterior)

    col_1, col_2, col_3, col_4 = st.columns(4)
    col_1.container(border=True).metric("Total de Organizações", orgs_ultimo_mes, delta_orgs)
    col_2.container(border=True).metric("Organizações com pacotes", tot_org_dados_ult, delta_org_dados)
    col_3.container(border=True).metric("Total de pacotes", tot_pacotes_ultimo_mes, delta_pacotes)
    col_4.container(border=True).metric("Total de recursos", int(tot_recursos_ultimo_mes), int(delta_recursos))


def preparar_dados_grafico(df, organizacao_selecionada):
    """Prepara os dados para o gráfico."""
    df_grafico = df.groupby(
        'nome_organizacao' if organizacao_selecionada == 'Selecionar tudo' else 'nome_pacote'
    ).agg({'qtd_recurso_pacote': 'sum'}).reset_index()

    df_grafico = df_grafico.rename(columns={
        'nome_organizacao': 'Organização',
        'qtd_recurso_pacote': 'Quantidade de Recursos',
        'nome_pacote': 'Pacote'
    }).sort_values(by="Quantidade de Recursos", ascending=False)

    df_grafico['Quantidade de Recursos'] = df_grafico['Quantidade de Recursos'].astype(int)
    return df_grafico


# --- Fluxo Principal ---
def fluxo_ckan():
    # Carregar dados e criar filtros
    df = main_ckan()

    data_atual_ckan, data_anterior_ckan, organizacao_selecionada = criar_filtros_ckan(df)
    df_atual, df_anterior = filtrar_dados(df, data_atual_ckan, data_anterior_ckan, organizacao_selecionada)

    # data_atual, data_anterior, organizacao_selecionada = criar_filtros_ckan(df)
    # df_atual, df_anterior = filtrar_dados(df, data_atual, data_anterior, organizacao_selecionada)

    # Exibir KPIs do CKAN
    st.header("Informações do Ckan")
    exibir_kpis_ckan(df_atual, df_anterior)

    # Preparar e exibir gráfico
    df_grafico = preparar_dados_grafico(df_atual, organizacao_selecionada)
    criar_tabela(df_grafico, df_grafico.columns[0], renomear=False)

    return df_atual, df_anterior, data_atual_ckan, data_anterior_ckan
