import os

ENDERECO_ALVO = "1JHH1pmHujcVa1aXjRrA13BJ13iCfgfBqj"

IGNORAR = [
    '1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s',
    '1HaTSjMb9Tg8yDNk5axvnWqyTUss26XUjV'
]

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(DIRETORIO_ATUAL, "dados_cache")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)