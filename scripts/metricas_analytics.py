import os
from datetime import timedelta, datetime
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

# Definir o caminho do arquivo de credenciais do Analytics

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\Kauã Rodrigo\Documents\scripts_python\monitoring_al_dados\data\credencias_analytics.json'


# --- Funções do Google Analytics ---
def executar_relatorio_analytics(property_id, data_inicial, data_final, dimensoes=None):
    """
    Executa um relatório no Google Analytics 4 e retorna uma lista de dicionários com métricas e dimensões.

    :param property_id: ID da propriedade do Google Analytics.
    :param data_inicial: Data inicial no formato "DD/MM/YYYY".
    :param data_final: Data final no formato "DD/MM/YYYY".
    :param dimensoes: Lista de dimensões a serem incluídas no relatório.
    :return: Lista de dicionários com métricas e dimensões.
    """
    client = BetaAnalyticsDataClient()

    # Converter datas para o formato YYYY-MM-DD
    data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y").strftime("%Y-%m-%d")
    data_final = datetime.strptime(data_final, "%d/%m/%Y").strftime("%Y-%m-%d")

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=dim) for dim in (dimensoes or [])],
        metrics=[
            Metric(name="activeUsers"),
            Metric(name="newUsers"),
            Metric(name="sessions"),
            Metric(name="engagedSessions"),
            Metric(name="engagementRate"),
            Metric(name="screenPageViews"),
            Metric(name="eventCount"),
        ],
        date_ranges=[DateRange(start_date=data_inicial, end_date=data_final)],
    )

    response = client.run_report(request)

    if not response.rows:
        raise ValueError(f"Nenhum dado retornado para o intervalo {data_inicial} a {data_final}.")

    # Processar os dados
    dados = []
    for row in response.rows:
        linha = {
            "Usuários Ativos": int(row.metric_values[0].value),
            "Novos Usuários": int(row.metric_values[1].value),
            "Sessões": int(row.metric_values[2].value),
            "Sessões Engajadas": int(row.metric_values[3].value),
            "Taxa de Engajamento": float(row.metric_values[4].value),
            "Páginas Visualizadas": int(row.metric_values[5].value),
            "Eventos": int(row.metric_values[6].value),
        }

        if dimensoes:
            for i, dim in enumerate(dimensoes):
                linha[dim] = row.dimension_values[i].value

        dados.append(linha)

    return dados


def carregar_metricas_analytics(property_id="366628261", data_anterior="01/09/2024", data_atual="30/09/2024"):
    """
    Carrega as métricas do Google Analytics e calcula as variações em relação ao período anterior.

    :param property_id: ID da propriedade do Google Analytics.
    :param data_anterior: Data inicial do período atual no formato "DD/MM/YYYY".
    :param data_atual: Data final do período atual no formato "DD/MM/YYYY".
    :return: Dois DataFrames, um com as métricas atuais e outro com as variações.
    """

    # Converter as datas para objetos datetime
    data_anterior_dt = datetime.strptime(data_anterior, "%d/%m/%Y").date()
    data_atual_dt = datetime.strptime(data_atual, "%d/%m/%Y").date()

    # Garantir que a data de início seja menor ou igual à data de fim
    if data_anterior_dt > data_atual_dt:
        raise ValueError(f"A data de início ({data_anterior}) não pode ser maior que a data de fim ({data_atual}).")

    # Calcular o intervalo do período atual
    intervalo = data_atual_dt - data_anterior_dt

    # Determinar o período anterior com base no intervalo
    data_atual_anterior_dt = data_anterior_dt - timedelta(days=1)
    data_anterior_anterior_dt = data_atual_anterior_dt - intervalo

    # Converter de volta para string no formato desejado
    data_anterior_anterior = data_anterior_anterior_dt.strftime("%d/%m/%Y")
    data_atual_anterior = data_atual_anterior_dt.strftime("%d/%m/%Y")

    # Obter métricas para o período atual
    metricas_atual = executar_relatorio_analytics(property_id, data_anterior, data_atual)

    # Obter métricas para o período anterior
    metricas_anterior = executar_relatorio_analytics(property_id, data_anterior_anterior, data_atual_anterior)

    # Calcular diferenças entre os períodos (deltas)
    deltas = {chave: metricas_atual[0][chave] - metricas_anterior[0][chave] for chave in metricas_atual[0].keys()}

    # Criar DataFrames
    df = pd.DataFrame([metricas_atual[0]])
    df_deltas = pd.DataFrame([deltas])

    return df, df_deltas, data_atual_anterior, data_anterior_anterior


def dimensoes_analytics(property_id="366628261", data_anterior="2024-09-01", data_atual="2024-09-30", dimensao=None):
    """
    Executa um relatório no Google Analytics 4 com dimensões específicas.

    :param property_id: ID da propriedade do Google Analytics.
    :param data_anterior: Data inicial no formato "DD/MM/YYYY".
    :param data_atual: Data final no formato "DD/MM/YYYY".
    :param dimensao: Lista de dimensões a serem incluídas no relatório.
    :return: DataFrame com métricas e dimensões.
    """
    metricas = executar_relatorio_analytics(property_id, data_anterior, data_atual, dimensao)
    return pd.DataFrame(metricas)
