# Real-Time Crypto Pipeline — CoinGecko API → Snowflake

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=flat&logo=snowflake&logoColor=white)
![Status](https://img.shields.io/badge/status-active-success?style=flat)

Pipeline automatisé qui ingère les prix de cryptomonnaies en temps réel
depuis l'API CoinGecko vers Snowflake, avec monitoring qualité des données.

## Architecture

```
CoinGecko API (toutes les 60s)
        │
        ▼
  Python Script
  (fetch + clean)
        │
        ▼
  Snowflake RAW
  RAW_CRYPTO_PRICES
        │
        ▼
  Vue Monitoring
  DATA_QUALITY_REPORT
```

## Stack technique

| Outil | Usage |
|---|---|
| Python 3.11 | Orchestration, appel API, insertion |
| requests | Appel API CoinGecko |
| Snowflake | Stockage des prix en temps réel |
| logging | Traçabilité des runs et erreurs |

## Fonctionnalités

- Ingestion automatique toutes les **60 secondes**
- **3 cryptos** suivies : Bitcoin, Ethereum, BNB
- **Logging** complet dans `pipeline.log`
- **Gestion des erreurs** : le pipeline continue même si un run échoue
- **Vue de monitoring** qualité dans Snowflake

## Résultats

```
15 lignes insérées (5 runs × 3 cryptos)
0 erreurs détectées
Latence moyenne : < 2 secondes par run
```

## Lancer le pipeline

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer les credentials
cp .env.example .env
# (remplir les valeurs dans .env)

# Lancer le pipeline
python scripts/pipeline_crypto.py
```

## Structure du projet

```
├── scripts/
│   └── pipeline_crypto.py    # Script principal
├── sql/
│   └── setup_snowflake.sql   # Création table + vue monitoring
├── screenshots/              # Preuves d'exécution
├── .env.example              # Template credentials
├── requirements.txt
└── README.md
```

## Certifications associées

- Snowflake Hands-On Essentials: Data Engineering Workshop
- Snowflake Hands-On Essentials: Data Warehousing Workshop
