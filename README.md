Plataforma de Inteligência de Mercado (Ecossistema NoSQL)
Este projeto foi desenvolvido como Desafio Final da disciplina de Banco de Dados NoSQL. A aplicação consiste em um backend em Python que orquestra quatro diferentes bancos de dados NoSQL para gerir cotações de criptoativos em tempo real.

🏗️ Arquitetura de Persistência Poliglota
O sistema utiliza a estratégia de "o banco certo para o problema certo":

Redis: Cache de baixíssima latência para cotações atuais (TTL de 10s).

MongoDB: Data Lake para armazenamento do log bruto (JSON) das requisições.

Cassandra: Banco de série temporal para histórico de preços, otimizado para consultas ordenadas por tempo.

Neo4j: Banco de grafos para mapear a rede de investidores e disparar alertas de monitoramento.

🚀 Como Executar
A aplicação foi totalmente containerizada para garantir que todas as dependências (incluindo drivers específicos de bancos de dados) funcionem de forma portável.

Pré-requisitos
Docker e Docker Compose instalados.

Passo a Passo
Clone este repositório.

No terminal, dentro da pasta do projeto, execute:

docker-compose up --build
O Docker irá subir os 4 bancos de dados e construir a imagem do script Python.

O script aguardará 30 segundos (tempo de inicialização do Cassandra/Neo4j) e iniciará o monitoramento automaticamente.

📊 Funcionalidades Implementadas
Setup Automático: O script cria os Keyspaces/Tabelas no Cassandra e os Nós/Relacionamentos no Neo4j caso não existam.

Lógica de Cache: Implementação de Cache Hit e Cache Miss para otimizar chamadas à API da Binance.

Tratamento de Erros: Conexão robusta com blocos try/except para garantir a estabilidade do ecossistema.

🔥 Bônus (Volatilidade): Lógica visual no terminal comparando o preço atual com o anterior (🟢 Subiu / 🔴 Caiu).

🛠️ Tecnologias Utilizadas
Python 3.12

Redis (Alpine)

MongoDB

Apache Cassandra

Neo4j (Cypher)

Docker & Docker Compose