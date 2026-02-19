import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
from config import ENDERECO_ALVO, DIRETORIO_ATUAL
from enderecos import pega_dados_endereco, verifica_tags
from analise import processa_transacoes, calcula_gini, analise_benford

def main():
    print("="*60)
    print("RELATÓRIO DE ANÁLISE FORENSE")
    print(f"Alvo: {ENDERECO_ALVO}")
    print("="*60)

    dados_raw = pega_dados_endereco(ENDERECO_ALVO)
    tags = verifica_tags(ENDERECO_ALVO)
    print("\n[1] FONTES CONHECIDAS")
    print(f"    Tags identificadas: {tags}")

    print("\n[2] PROCESSAMENTO DE DADOS")
    print("     Analisando blockchain e construindo grafos...")
    valores, grafo_h1, grafo_fluxo, trocos = processa_transacoes(dados_raw)
    array_valores = np.array(valores)

    print("\n[3] PERFIL FINANCEIRO DO ENDEREÇO")
    print(f"    Total de Transações Analisadas: {len(valores)}")
    if len(valores) > 0:
        print(f"    Volume Total Recebido: {np.sum(array_valores):,.0f} Satoshis")
        print(f"    Média por Transação:   {np.mean(array_valores):,.2f}")
        print(f"    Mínimo Recebido:       {np.min(array_valores)}")
        print(f"    Máximo Recebido:       {np.max(array_valores)}")
        print(f"    Coeficiente de Gini:   {calcula_gini(array_valores):.4f}")
        print("     (Gini > 0,8 indica alta concentração/desigualdade)")

    print("\n[4] ANÁLISE DE BENFORD (Detecção de Anomalias)")
    benford = analise_benford(array_valores)
    print("     Dígito | Frequência Real| Esperado (Benford)")
    print("     -------+----------------+-------------------")
    esperado = {1: 0.301, 2: 0.176, 3: 0.125}
    for d in [1, 2, 3]:
        real = benford.get(d, 0)
        print(f"    {d} |   {real:.3f}  |   {esperado[d]}")

    print("\n[5] ANÁLISE DE ENTIDADES (Clusterização H1 + Troco)")
    clusters = list(nx.connected_components(grafo_h1))
    print(f"    Total de Depositantes Únicos: {len(grafo_fluxo.nodes()) - 1}")
    print(f"    Entidades Reais Estimadas (Clusters): {len(clusters)}")
    maior_cluster = 0
    if clusters:
        maior_cluster = len(max(clusters, key=len))
        print(f"    Maior Entidade controla {maior_cluster} endereços.")        
    print(f"    Transações com identificação de troco: {len(trocos)}")

    print("\n[6] GERANDO VISUALIZAÇÃO GRÁFICA...")
    plt.figure(figsize=(16, 14))
    centro = [ENDERECO_ALVO]
    outros_nos = [node for node in grafo_fluxo.nodes() if node != ENDERECO_ALVO]
    shells= [centro, outros_nos]

    pos = nx.shell_layout(grafo_fluxo, nlist=shells)

    cor_node = ['red' if node == ENDERECO_ALVO else 'blue' for node in grafo_fluxo.nodes()]
    tamanho_node = [1200 if node == ENDERECO_ALVO else 350 for node in grafo_fluxo.nodes()]

    pesos_dict = nx.get_edge_attributes(grafo_fluxo, 'weight')
    espessuras = [max(0.5, np.log1p(w) * 1.5) for w in pesos_dict.values()] if pesos_dict else 1.0
    rotulos_nos = {node: f"{node[:6]}..." if node != ENDERECO_ALVO else "ALVO\nFaraó" for node in grafo_fluxo.nodes()}

    nx.draw(grafo_fluxo, pos,
            node_color=cor_node,
            node_size=tamanho_node,
            edge_color='gray',
            width=espessuras,
            alpha=0.6,
            labels=rotulos_nos,
            with_labels=True,
            font_size=9,
            font_weight='bold',
            arrows=True,
            arrowsize=15
            )
    
    rotulos_arestas = {aresta: f"{peso:.2f} BTC" for aresta, peso in pesos_dict.items()}
    nx.draw_networkx_edge_labels(
        grafo_fluxo, pos,
        edge_labels=rotulos_arestas,
        font_color='black',
        font_size=8,
        label_pos=0.25,
        bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)
        )
    
    plt.title(f"Fluxo Financeiro: Faraó do Bitcoin\n(Endereço: {ENDERECO_ALVO[:10]}...)\nDetectados {len(trocos)} endereços de troco")
    caminho_imagem = os.path.join(DIRETORIO_ATUAL, "relatorio_grafo.png")
    plt.savefig(caminho_imagem, dpi=300, bbox_inches='tight')
    print(f"     Gráfico salvo com sucesso em: {caminho_imagem}")
    plt.show()

if __name__ == "__main__":
    main()