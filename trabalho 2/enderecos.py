import json
import time
import os
import requests
from config import DATA_DIR, IGNORAR

def pega_dados_endereco(endereco):
    """
    Consulta a API do blockchain.com com cache local e delay
    """
    file_path = os.path.join(DATA_DIR, f"{endereco}.json")

    if os.path.exists(file_path):
        print(f"Carregando dados locais de {endereco}...")
        with open(file_path, 'r') as f:
            return json.load(f)
        
    print(f"Baixando dados de {endereco}...")
    url = f"https://blockchain.info/rawaddr/{endereco}"

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            data = resposta.json()
            with open(file_path, 'w') as f:
                json.dump(data, f)

            time.sleep(5)
            return data
        else:
            print(f"Erro {resposta.status_code} ao baixar {endereco}")
            return None
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None
    
def filtra_endereco(end):
    """
    Retorna True se o endereço for válido para análise (não é exchange).
    """
    if end in IGNORAR:
        return False
    if not (end.startswith('1') or end.startswith('bc1')):
        return False
    return True

def verifica_tags(endereco):
    """
    Simula uma busca em base de dados de tags.
    Para o trabalho, podemos identificar manualmente o alvo conhecido.
    """
    tags_conhecidas = {
        "1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj": "G.A.S. Consultoria / Glaidson Acácio",
        "1HaTSjMb9Tg8yDNk5axvnWqyTUss26XUjV": "Exchange (Binance/Huobi) - Ignorado"
    }
    return tags_conhecidas.get(endereco, "Sem tags registradas")
