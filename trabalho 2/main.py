import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from config import ENDERECO_ALVO
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
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(grafo_fluxo, k=0.15, iterations=20)

    cor_node = ['red' if node == ENDERECO_ALVO else 'blue' for node in grafo_fluxo.nodes()]
    tamanho_node = [500 if node == ENDERECO_ALVO else 30 for node in grafo_fluxo.nodes()]

    rotulos = False
    if len(grafo_fluxo.nodes()) < 50:
        rotulos = True

    nx.draw(grafo_fluxo, pos,
            node_color=cor_node,
            node_size=tamanho_node,
            edge_color='gray',
            width=0.5,
            alpha=0.6,
            with_labels=rotulos,
            arrows=True)
    
    plt.title(f"Fluxo Financeiro: Faraó do Bitcoin\n(Endereço: {ENDERECO_ALVO[:10]}...)\nDetectados {len(trocos)} endereços de troco")
    plt.savefig("relatorio_grafo.png")
    print("     Gráfico salvo como 'relatorio_grafo.png'")
    plt.show()

if __name__ == "__main__":
    main()