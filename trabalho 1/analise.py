import pandas as pd
import numpy as np
import glob
import os

pasta_dados = 'mar'
padrao_arquivo = '*.tsv'
num_permuta = 5000

def carregar_mes_inteiro(pasta):
    print(f"Lendo a pasta {pasta}...")
    arquivos = glob.glob(os.path.join(pasta, padrao_arquivo))
    arquivos.sort()

    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo .tsv encontrado na pasta '{pasta}'")
    
    print(f"Encontrados {len(arquivos)} arquivos diários. Concatenando...")

    lista_dfs = []
    for arq in arquivos:
        try:
            df_temp = pd.read_csv(arq, sep='\t', usecols=['id', 'time', 'guessed_miner'])
            lista_dfs.append(df_temp)
        except Exception as e:
            print(f"Erro ao ler {arq}: {e}")

    df_mes = pd.concat(lista_dfs, ignore_index=True)
    df_mes = df_mes.sort_values('id').reset_index(drop=True)
    df_mes['guessed_miner'] = df_mes['guessed_miner'].fillna('Unknown')
    print(f"Base de dados completa montada: {len(df_mes)} blocos processados.")
    return df_mes

def analisar_streaks(df):
    top_miner = df['guessed_miner'].value_counts().idxmax()
    count = df['guessed_miner'].value_counts().max()
    print(f"\nAlvo da Análise: {top_miner} ({count} blocos)")

    sequencia_real = df['guessed_miner'].values
    streak_real = calcular_eventos_streak(sequencia_real, top_miner)
    print(f"Sequências consecutivas observadas: {streak_real}")

    print(f"Rodando {num_permuta} permutações...")
    permutacoes = []
    sequencia_temp = sequencia_real.copy()

    for _ in range(num_permuta):
        np.random.shuffle(sequencia_temp)
        permutacoes.append(calcular_eventos_streak(sequencia_temp, top_miner))

    permutacoes = np.array(permutacoes)
    media_esperada = np.mean(permutacoes)
    prob_sorte = np.sum(permutacoes >= streak_real)/num_permuta
    print("\n----- RESULTADOS ESTATÍSTICOS -----")
    print(f"Média esperada: {media_esperada:.2f}")
    print(f"Valor observado: {streak_real}")
    print(f"Probabilidade de ser mera sorte: {prob_sorte:.5f}")

    interpretacao(prob_sorte, top_miner)


def calcular_eventos_streak(sequencia, alvo):
    is_target = (sequencia == alvo)
    s = pd.Series(is_target)
    grupos = s.ne(s.shift()).cumsum()
    contagem = 0
    grouped = s.groupby(grupos)
    tamanhos = grouped.size()
    valores = grouped.first()
    contagem = ((valores == True) & (tamanhos >= 2)).sum()
    return contagem

def interpretacao(p, miner):
    print("\n----- CONCLUSÃO -----")
    if p < 0.05:
        print(f"ALERTA DE ANOMALIA!!!!! A probabilidade de ser sorte pura é {p:.5f}")
        print(f"O minerador {miner} tem uma capacidade irreal de encontrar blocos em sequência, o que fortemente indica Mineração Egoísta.")
    else:
        print(f"Comportamente Normal, já que a probabilidade de ser sorte é {p:.5f}")
        print(f"As sequências de {miner} estão dentro do esperado para o seu poder computacional, não aparenta ser Mineração Egoísta")

if __name__ == "__main__":
    try:
        df_completo = carregar_mes_inteiro(pasta_dados)
        analisar_streaks(df_completo)
    except Exception as e:
        print(f"Erro fatal: {e}")