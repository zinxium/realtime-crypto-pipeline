import os
import time
import logging
import requests
import pandas as pd
import snowflake.connector
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()          # affiche aussi dans le terminal
    ]
)
log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────
API_URL = (
    "https://api.coingecko.com/api/v3/coins/markets"
    "?vs_currency=usd"
    "&ids=bitcoin,ethereum,binancecoin"
    "&order=market_cap_desc"
)
INTERVAL_SECONDS = 60   # on appelle l'API toutes les 60 secondes
MAX_RUNS         = 5    # on fait 5 appels puis on s'arrête (pour le test)

# ── Connexion Snowflake ───────────────────────────────────────
def get_connection():
    return snowflake.connector.connect(
        account=os.getenv("SF_ACCOUNT"),
        user=os.getenv("SF_USER"),
        password=os.getenv("SF_PASSWORD"),
        warehouse=os.getenv("SF_WAREHOUSE"),
        database=os.getenv("SF_DATABASE"),
        schema=os.getenv("SF_SCHEMA"),
    )

# ── Appel API CoinGecko ───────────────────────────────────────
def fetch_crypto_prices():
    log.info("Appel API CoinGecko...")
    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    log.info(f"  {len(data)} cryptos récupérées")
    return data

# ── Insertion dans Snowflake ──────────────────────────────────
def insert_to_snowflake(conn, records):
    sql = """
        INSERT INTO RAW_CRYPTO_PRICES (
            id, symbol, name, current_price,
            market_cap, total_volume,
            price_change_24h, price_change_pct, last_updated
        ) VALUES (
            %(id)s, %(symbol)s, %(name)s, %(current_price)s,
            %(market_cap)s, %(total_volume)s,
            %(price_change_24h)s, %(price_change_percentage_24h)s,
            %(last_updated)s
        )
    """
    cur = conn.cursor()
    for r in records:
        cur.execute(sql, r)
    conn.commit()
    log.info(f"  {len(records)} lignes insérées dans Snowflake")

# ── Pipeline principal ────────────────────────────────────────
def run_pipeline():
    log.info("=== Démarrage du pipeline crypto ===")
    conn = get_connection()
    log.info("Connecté à Snowflake")

    for i in range(1, MAX_RUNS + 1):
        log.info(f"--- Run {i}/{MAX_RUNS} ---")
        try:
            records = fetch_crypto_prices()
            insert_to_snowflake(conn, records)
            log.info(f"  Run {i} terminé avec succès")
        except Exception as e:
            log.error(f"  Erreur run {i} : {e}")

        if i < MAX_RUNS:
            log.info(f"  Attente {INTERVAL_SECONDS}s avant le prochain run...")
            time.sleep(INTERVAL_SECONDS)

    conn.close()
    log.info("=== Pipeline terminé. Connexion fermée. ===")

if __name__ == "__main__":
    run_pipeline()