# Bitcoin Selfish Mining Detector (Permutation Test)

Este projeto é uma ferramenta de forense digital para blockchain que analisa dados históricos do Bitcoin para detectar anomalias estatísticas compatíveis com **Mineração Egoísta** (*Selfish Mining*).

O script processa grandes volumes de dados de blocos (dumps do Blockchair), reconstrói a linha do tempo mensal e aplica um **Teste de Permutação (Monte Carlo)** para verificar se as sequências de vitórias (*winning streaks*) de um minerador são fruto de sorte ou de um comportamento estratégico anômalo.

## 📋 Sobre o Projeto

A **Mineração Egoísta** é um ataque teórico onde um minerador (ou pool) retém blocos descobertos para si mesmo e os libera estrategicamente para invalidar os blocos de mineradores honestos. Uma das "assinaturas" estatísticas desse ataque é uma frequência anormalmente alta de blocos consecutivos minerados pela mesma entidade.

Este software:
1.  Ingere dados diários brutos (TSV) da blockchain.
2.  Unifica e ordena os dados cronologicamente.
3.  Identifica o minerador dominante (maior hashrate).
4.  Calcula a frequência de sequências consecutivas (streaks ≥ 2).
5.  Executa milhares de permutações aleatórias para calcular o **P-Valor**.

## 🛠️ Tecnologias Utilizadas

* **Python 3.8+**
* **Pandas:** Para manipulação de DataFrames e leitura eficiente de arquivos TSV.
* **NumPy:** Para cálculos matemáticos e simulação de Monte Carlo.

## 📂 Estrutura de Arquivos

O script espera que os dados estejam organizados da seguinte forma:

```text
/
├── mes.py             # script para determinar o mês da análise
├── main.py            # O script principal de análise
├── README.md          # Este arquivo
└── mar/               # Pasta contendo os arquivos diários do mês
    ├── blockchair_bitcoin_blocks_20250301.tsv
    ├── blockchair_bitcoin_blocks_20250302.tsv
    └── ... (até o dia 31)

