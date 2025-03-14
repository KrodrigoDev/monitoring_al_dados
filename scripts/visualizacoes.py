import streamlit as st


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
