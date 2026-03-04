# 🚀 Plataforma de Inteligência de Mercado (NoSQL)

Este projeto foi desenvolvido para a disciplina de **Banco de Dados NoSQL**. O sistema consiste em um monitor de ativos financeiros (Criptomoedas) que utiliza uma arquitetura de **Persistência Poliglota** para garantir escalabilidade e performance.

---

## 🏗️ Arquitetura do Ecossistema
O sistema orquestra quatro bancos de dados simultaneamente, utilizando cada um para sua especialidade técnica:

* **⚡ Redis**: Camada de `Cache` de baixíssima latência. Armazena a cotação atual com **TTL de 10 segundos** para evitar chamadas desnecessárias à API.
* **🍃 MongoDB**: Atua como `Data Lake`. Armazena o documento JSON bruto de cada coleta, incluindo o campo `data_coleta` para auditoria futura.
* **📊 Cassandra**: Especializado em `Série Temporal`. Armazena o histórico de preços em uma tabela modelada com *Partition Key* e *Clustering Key* para buscas rápidas e ordenadas.
* **🕸️ Neo4j**: Banco de `Grafos` que mapeia a rede de investidores. Utiliza queries **Cypher** para identificar quais usuários devem ser notificados sobre mudanças no preço.

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem**: `Python 3.12` (executado via Docker).
* **Orquestração**: `Docker` & `Docker Compose`.
* **Bancos**: `Redis`, `MongoDB`, `Cassandra`, `Neo4j`.
* **API**: `Binance Public Data` (Bitcoin - BTCUSDT - https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT).

---

## 🚀 Como Executar o Projeto

Para garantir a portabilidade (visto que alguns drivers NoSQL possuem dependências complexas), o projeto foi totalmente **containerizado**.

1. **Certifique-se de que o Docker Desktop está rodando.**
2. **No terminal, dentro da pasta do projeto, execute:**
   ```bash
   docker-compose up --build
   Aguarde a inicialização: O script Python possui um delay de 30 segundos no início para garantir que o Cassandra e o Neo4j estejam prontos para receber conexões.

🌟 Diferenciais Implementados (Bônus)
🟢/🔴 Lógica de Volatilidade: O terminal exibe visualmente se o preço subiu ou caiu em relação à última leitura do cache.

🛡️ Resiliência: Implementação de blocos try/except para conexões robustas com os containers.

⚙️ Setup Automático: O script cria automaticamente os Keyspaces, Tabelas e Nós de investidores na primeira execução.

Desenvolvido por: [Carlos Emanuel de Sousa Silva]