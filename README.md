# Análises Forenses em Bitcoin e Blockchain

Este repositório contém projetos de forense digital e análise de dados focados na blockchain do Bitcoin. O código está dividido em dois trabalhos principais que exploram diferentes vertentes de análise de rede, deteção de anomalias na mineração e comportamento estatístico de transações.

## 📂 Estrutura do Repositório

* **`trabalho 1/`**: Focado na deteção de anomalias estatísticas compatíveis com *Selfish Mining*.
* **`trabalho 2/`**: Focado na análise forense, clusterização e rastreio do fluxo financeiro de um endereço de Bitcoin específico.

---

## ⛏️ Trabalho 1: Detetor de Mineração Egoísta (Selfish Mining)

Este projeto é uma ferramenta digital que analisa dados históricos do Bitcoin para detetar uma das assinaturas do ataque de Mineração Egoísta (*Selfish Mining*): uma frequência anormalmente alta de blocos consecutivos minerados pela mesma entidade. 

O script processa grandes volumes de dados de blocos em formato TSV, reconstrói a linha do tempo e aplica um **Teste de Permutação (Monte Carlo)**.

### Como Funciona
1. **Ingestão de Dados:** Lê e concatena ficheiros diários contendo o ID, o tempo e o provável minerador do bloco.
2. **Cálculo de *Streaks*:** Identifica o minerador dominante e calcula o número de eventos em que o mesmo extraiu blocos consecutivos.
3. **Avaliação Estatística:** Executa 5000 permutações aleatórias da sequência de blocos para calcular a probabilidade (P-Valor) daquela sequência de vitórias ocorrer por mera sorte.

---

## 🔍 Trabalho 2: Análise Forense Financeira ("O Faraó do Bitcoin")

O segundo projeto é um script de investigação focado nas transações de um endereço alvo (identificado no ficheiro `config.py`). O sistema traça o perfil financeiro, deteta anomalias e desenha grafos de interação para inferir o tamanho e controlo das entidades financeiras na blockchain.

### Como Funciona
1. **Processamento de Redes:** A partir de ficheiros JSON com dados brutos das transações, constrói grafos de fluxo direcionado e grafos de correlação de entidades.
2. **Perfil Financeiro e Gini:** Calcula estatísticas agregadas (volume recebido, médias, picos) e utiliza o **Coeficiente de Gini** para medir o nível de desigualdade/concentração das entradas financeiras recebidas no endereço.
3. **Teste de Benford:** Aplica a Análise da Lei de Benford sobre o primeiro dígito dos valores depositados para avaliar discrepâncias suspeitas comparando a frequência real com a esperada.
4. **Clusterização de Entidades:** Utiliza a heurística de multi-input (H1) aliada à deteção de endereços de troco para tentar associar endereços avulsos a utilizadores/entidades únicas.
5. **Visualização Gráfica:** Renderiza o fluxo financeiro através da biblioteca e exporta a rede no ficheiro de imagem `relatorio_grafo.png`.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.8+**
* **Pandas:** Para manipulação de DataFrames e leitura eficiente de ficheiros.
* **NumPy:** Para cálculo matricial e de métricas estatísticas de distribuição.
* **NetworkX:** Para criação e análise avançada das topologias em grafos.
* **Matplotlib:** Para renderização visual da rede de transações gerada.
