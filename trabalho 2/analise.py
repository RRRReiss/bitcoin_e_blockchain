import numpy as np
import pandas as pd
import networkx as nx
from enderecos import filtra_endereco
from config import ENDERECO_ALVO, IGNORAR

def calcula_gini(valores):
    """
    Calcula o coeficiente de Gini
    """
    if len(valores) == 0: return 0
    array = np.sort(valores)
    index = np.arange(1, array.shape[0]+1)
    n = array.shape[0]
    return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

def analise_benford(valores):
    """
    Retorna a distribuição do primeiro dígito
    """
    primeiros_digitos = [int(str(v)[0]) for v in valores if v > 0]
    if not primeiros_digitos: return pd.Series()
    return pd.Series(primeiros_digitos).value_counts(normalize=True).sort_index()

def processa_transacoes(data):
    """
    Lê o JSON bruto e gera as estruturas para análise.
    Retorna: (lista_valores, grafo_h1, grafo_fluxo, lista_troco)
    """
    valores_entrada = []
    grafo_h1 = nx.Graph()
    grafo_fluxo = nx.DiGraph()
    possivel_troco = []

    if not data:
        return [], grafo_h1, grafo_fluxo, []
    
    for tx in data['txs']:
        outputs = tx['out']
        eh_deposito = False
        valor_recebido_nesta_tx = 0

        for out in outputs:
            if out.get('addr') == ENDERECO_ALVO:
                eh_deposito = True
                valor_recebido_nesta_tx += out.get('value', 0)
                valores_entrada.append(out.get('value', 0))

        if eh_deposito:
            tx_inputs = []
            for inp in tx['inputs']:
                remetente = inp.get('prev_out', {}).get('addr')
                valor_input_btc = inp.get('prev_out', {}).get('value', 0)/100000000
                if remetente and filtra_endereco(remetente):
                    tx_inputs.append(remetente)
                    grafo_fluxo.add_edge(remetente, ENDERECO_ALVO, tx=tx['hash'], weight=valor_input_btc)

            if len(tx_inputs) > 1:
                for i in range(len(tx_inputs) - 1):
                    grafo_h1.add_edge(tx_inputs[i], tx_inputs[i+1])

            if len(outputs) == 2:
                for out in outputs:
                    addr = out.get('addr')
                    if addr != ENDERECO_ALVO and addr not in IGNORAR:
                        possivel_troco.append({
                            'tx': tx['hash'],
                            'suspect_change': addr,
                            'value': out.get('value')
                        })

                        if len(tx_inputs) > 0:
                            grafo_h1.add_edge(tx_inputs[0], addr)

    return valores_entrada, grafo_h1, grafo_fluxo, possivel_troco