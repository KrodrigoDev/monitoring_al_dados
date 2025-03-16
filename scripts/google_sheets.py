import os.path

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "15YLcvrUy3ZhmplKMYJPxKDyBTkSyTsEBhVViOdfKzC8"
SHEET_RANGE = "Página1!A:D"


def consumir_dados():
    service = criar_conexao()
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE)
        .execute()
    )
    values = result.get("values", [])

    df = pd.DataFrame(values, columns=values[0])
    df = df.drop(index=0).reset_index(drop=True)

    return df


def criar_conexao():
    creds = None
    if os.path.exists("../monitoring_al_dados/data/token.json"):
        creds = Credentials.from_authorized_user_file("../monitoring_al_dados/data/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("../monitoring_al_dados/data/client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("../monitoring_al_dados/data/token.json", "w") as token:
            token.write(creds.to_json())
    return build("sheets", "v4", credentials=creds)


def atualizar_planilha(novos_valores):
    service = criar_conexao()

    sheet = service.spreadsheets()
    body = {"values": novos_valores}
    try:
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=SHEET_RANGE,
            valueInputOption="RAW",
            body=body
        ).execute()
        print("Planilha atualizada com sucesso!")
    except HttpError as err:
        print(f"Erro ao atualizar a planilha: {err}")
