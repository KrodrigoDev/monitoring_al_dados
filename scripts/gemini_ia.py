import google.generativeai as genai
import pandas as pd
from dotenv import dotenv_values
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from io import BytesIO
import re

API_KEY_GEMINI = dotenv_values('../monitoring_al_dados/data/credenciais.env')['API_KEY_GEMINI']


def gerar_resumo(df_ckan, df_analytics, df_deltas, data_atual_ckan, data_anterior_ckan, data_atual_analytics,
                 data_anterior_analytics, data_inicio_anterior, data_fim_anterior):
    """
    Gera um resumo com base nos dados do CKAN e do Google Analytics, destacando tendências e insights.
    """
    genai.configure(api_key=API_KEY_GEMINI)

    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Você é um analista de dados. Resuma o relatório abaixo, destacando tendências e mudanças entre os períodos comparados:

    **Período CKAN:** {data_anterior_ckan} até {data_atual_ckan}
    **Período Analytics:** {data_anterior_analytics} até {data_atual_analytics} em comparação ao período de {data_inicio_anterior} até {data_fim_anterior}

    **Dados do CKAN:**
    - Total de Organizações: {df_ckan['Total de Organizações']}
    - Organizações com Pacotes: {df_ckan['Organizações com pacotes']}
    - Total de Pacotes: {df_ckan['Total de pacotes']}
    - Total de Recursos: {df_ckan['Total de recursos']}

    **Variação (Delta) do CKAN:**
    - Δ Organizações: {df_deltas['delta_orgs']}
    - Δ Pacotes: {df_deltas['delta_pacotes']}
    - Δ Recursos: {df_deltas['delta_recursos']}

    **Métricas do Google Analytics:**
    - Usuários Ativos: {df_analytics['Usuários Ativos']}
    - Novos Usuários: {df_analytics['Novos Usuários']}
    - Sessões: {df_analytics['Sessões']}
    - Sessões Engajadas: {df_analytics['Sessões Engajadas']}
    - Taxa de Engajamento: {df_analytics['Taxa de Engajamento']}%
    - Páginas Visualizadas: {df_analytics['Páginas Visualizadas']}
    - Eventos: {df_analytics['Eventos']}

    **Variação (Delta) do Analytics:**
    - Δ Usuários Ativos: {df_deltas['delta_usuarios_ativos']}
    - Δ Sessões: {df_deltas['delta_sessoes']}
    - Δ Taxa de Engajamento: {df_deltas['delta_taxa_engajamento']}%
    - Δ Páginas Visualizadas: {df_deltas['delta_paginas_visualizadas']}

    Gere um resumo destacando tendências e insights baseados nas mudanças observadas.
    """

    response = model.generate_content(prompt)
    return response.text


def formatar_texto_para_pdf(texto):
    """
    Converte a formatação Markdown (**negrito**) para HTML (<b>negrito</b>)
    para que o ReportLab interprete corretamente.
    """
    texto_formatado = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", texto)  # Substitui **texto** por <b>texto</b>
    texto_formatado = texto_formatado.replace("\n", "<br/>")  # Mantém quebras de linha
    return texto_formatado


def gerar_resumo_e_pdf(gemini_ia, df_ckan, df_analytics, df_deltas, data_atual_ckan, data_anterior_ckan,
                       data_atual_analytics,
                       data_anterior_analytics, data_inicio_anterior, data_fim_anterior):
    # Adiciona uma variável para controlar o estado de clique do botão
    resumo_gerado = None

    if st.button("Gerar resumo usando IA"):
        resumo_gerado = gemini_ia.gerar_resumo(
            df_ckan=df_ckan,
            df_analytics=df_analytics,
            df_deltas=df_deltas,
            data_atual_ckan=data_atual_ckan,
            data_anterior_ckan=data_anterior_ckan,
            data_atual_analytics=data_atual_analytics,
            data_anterior_analytics=data_anterior_analytics,
            data_inicio_anterior=data_inicio_anterior,
            data_fim_anterior=data_fim_anterior
        )
        # st.write(resumo_gerado)

    # Verifique se o resumo foi gerado
    if resumo_gerado:
        # Criar buffer de memória para PDF
        pdf_buffer = BytesIO()

        # Criar documento PDF
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Criar estilos personalizados
        title_style = ParagraphStyle(
            name="TitleStyle",
            parent=styles["Title"],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue
        )

        normal_style = ParagraphStyle(
            name="NormalStyle",
            parent=styles["BodyText"],
            fontSize=12,
            leading=16
        )

        # Baixar a imagem
        img_buffer = '../monitoring_al_dados/images/logo-dados-informacoes-azul.png'
        if img_buffer:
            logo = Image(img_buffer, width=200, height=60)  # Ajustar o tamanho conforme necessário
        else:
            logo = None

        # Criar conteúdo do PDF
        content = []
        if logo:
            content.append(logo)
        content.append(Spacer(1, 12))
        content.append(Paragraph("Resumo do Relatório de Dados", title_style))
        content.append(Spacer(1, 12))
        content.append(Paragraph(resumo_gerado.replace("\n", "<br/>"), normal_style))  # Respeitar quebras de linha

        # Aplicar formatação no resumo antes de adicionar ao PDF
        resumo_formatado = formatar_texto_para_pdf(resumo_gerado)
        content[-1] = (Paragraph(resumo_formatado, normal_style))

        doc.build(content)

        # Criar botão para baixar o PDF
        st.download_button(
            label="Salvar Resumo",
            data=pdf_buffer.getvalue(),
            file_name="Resumo_Geral.pdf",
            mime="application/pdf"
        )
