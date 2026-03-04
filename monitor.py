import time
import requests
import redis
from pymongo import MongoClient
from cassandra.cluster import Cluster
from neo4j import GraphDatabase
from datetime import datetime

print("[START] Aguardando 30s para inicialização dos bancos...")
time.sleep(30)

try:
    #Redis - Cache
    r = redis.Redis(host="redis", port=6379, decode_responses=True)

    #MongoDB - Data Lake
    mongo_client = MongoClient("mongodb://mongodb:27017/")
    db_mongo = mongo_client["fintech_db"]

    #Cassandra - Série Temporal
    cassandra_cluster = Cluster(["cassandra"])
    session_cassandra = cassandra_cluster.connect()

    #Neo4j - Grafo
    neo4j_driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password123"))

    print("[OK] Conexões estabelecidas")
except Exception as e:
    print(f"[ERRO] Falha ao conectar nos bancos: {e}")
    exit()

def setup_databases():
    print("[SETUP] Configurando esquemas iniciais...")

    #Cassandra: Keyspace e tabela
    session_cassandra.execute("""
        CREATE KEYSPACE IF NOT EXISTS market_data
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
    """)
    session_cassandra.execute("USE market_data")
    session_cassandra.execute("""
        CREATE TABLE IF NOT EXISTS historico_precos (
            moeda text,
            horario timestamp,
            preco decimal,
            PRIMARY KEY (moeda, horario)
        ) WITH CLUSTERING ORDER BY (horario DESC)
    """)

    #Neo4j: Investidores e Relacionamentos (Fase 1)
    with neo4j_driver.session() as session:
        investidores = ["Alice", "Bob", "Carlos"]
        for nome in investidores:
            session.run("""
                MERGE (i:Investidor {nome: $nome})
                MERGE (m:Moeda {simbolo: 'BTCUSDT'})
                MERGE (i)-[:ACOMPANHA]->(m)
            """, nome=nome)
    print("[SETUP] Pronto!")


def monitorar():
    setup_databases()
    symbol = "BTCUSDT"

    while True:
        print(f"\nConsultando preço do Bitcoin ({symbol})...")

        #lógica de cache (redis)
        cached_price = r.get(symbol)
        preco_anterior = r.get(f"{symbol}_last")

        if cached_price:
            print(f"[REDIS] Cache Hit. Valor Recuperado: {cached_price}")
            price = float(cached_price)
            data_origem = "Cache"
        else:
            print(f"[REDIS] Cache Miss! Fui na API da Binance.")
            try:
                res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
                data = res.json()
                price = float(data["price"])

                #salva no redis com TTL de 10 segundos
                r.setex(symbol, 10, str(price))
                data_origem = "API"

                #Data lake (mongdb)
                data["data_coleta"] = datetime.now()
                db_mongo.cotacoes_brutas.insert_one(data)
                print(f"[MONGO] Payload bruto salvo no Data Lake.")
            except Exception as e:
                print(f"Erro ao buscar API: {e}")
                continue

            #Serie temporal (cassandra)
            session_cassandra.execute(
                "INSERT INTO historico_precos (moeda, horario, preco) VALUES (%s, %s, %s)",
                (symbol, datetime.now(), price)
            )

            #lógica de volatilidade
            seta = ""
            if preco_anterior:
                p_ant = float(preco_anterior)
                if price > p_ant: seta = "🟢 (Subiu)"
                elif price < p_ant: seta = "🔴 (Caiu)"
                else: seta = "🟡 (Estável)"

            r.set(f"{symbol}_last", str(price)) #atualiza para a próxima comparação
            print(f"[CASSANDRA] Preço de ${price:,.2f} {seta} gravado na série temporal.")

            #Sistema de alertas (Neo4j)
            with neo4j_driver.session() as session:
                result = session.run("""
                    MATCH (i:Investidor)-[:ACOMPANHA]->(m:Moeda {simbolo: $simbolo})
                    RETURN i.nome AS nome
                """, simbolo=symbol)
                nomes = [record["nome"] for record in result]
                print(f"[NEO4J] Notificando investidores: {', '.join(nomes)}")

            time.sleep(15)

if __name__ == "__main__":
    monitorar()
    