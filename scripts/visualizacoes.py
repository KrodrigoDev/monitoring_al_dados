import streamlit as st
import altair as alt


def criar_tabela(df, coluna, renomeada='', renomear=False):
    if renomear:
        df = df.rename(columns={coluna: renomeada})
        coluna = renomeada
    colunas_ordenadas = [coluna] + [col for col in df.columns if col != coluna]
    df = df[colunas_ordenadas]

    column_config = {}

    # Identifica todas as colunas numéricas para aplicar barras de progresso
    for coluna in df.select_dtypes(include=['number']).columns:
        column_config[coluna] = st.column_config.ProgressColumn(
            label=coluna.replace("_", " ").title(),  # Formata nome da coluna
            format="%d",
            min_value=int(df[coluna].min()),
            max_value=int(df[coluna].max())
        )

    st.data_editor(df, column_config=column_config, hide_index=True, use_container_width=True)


def exibir_tabela_com_dimensao(titulo, df, coluna_dimensao, nome_legenda):
    """
    Exibe uma tabela desagregada por uma dimensão específica.
    """
    st.subheader(titulo)
    df.rename(columns={coluna_dimensao: nome_legenda}, inplace=True)

    # Exibição alternativa para melhor leitura
    st.table(df)


def criar_grafico(df, eixo_y, titulo):
    """
    Cria um gráfico de barras interativo com Altair.
    """
    df = df.sort_values(by='Quantidade de Recursos', ascending=False)  # Ordenação automática
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Quantidade de Recursos:Q', title=''),
        y=alt.Y(eixo_y, sort='-x', title=titulo),
        color=alt.Color(eixo_y, scale=alt.Scale(scheme='category20b')),
        tooltip=[alt.Tooltip(eixo_y, title=titulo), alt.Tooltip('Quantidade de Recursos', title='Qtd Recursos')]
    ).interactive()  # Torna o gráfico interativo

    st.altair_chart(chart, use_container_width=True)