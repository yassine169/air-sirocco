"""Santé des données : les données sont-elles fraîches et complètes ?

Ce script est lancé à la fin du pipeline. Il affiche un petit rapport
et s'arrête en ERREUR (code 1) si un problème est détecté.
"""
import os
import sys
from datetime import datetime, timedelta, timezone

import duckdb

# Sous Windows, la console peut être en cp1252 : sans ça, les emojis ✅/❌
# font planter le script (faux échec avec le code 1).
sys.stdout.reconfigure(encoding="utf-8")

DB = os.getenv("DUCKDB_PATH", "data/warehouse.duckdb")
NB_VILLES = 5
MAX_AGE = timedelta(hours=26)  # pipeline quotidien + 2h de marge

problemes = []
con = duckdb.connect(DB, read_only=True)

print("=== Rapport de santé des données ===")
for table in ["air_quality", "weather"]:
    nb_lignes, nb_villes, dernier = con.execute(f"""
        select count(*), count(distinct city), max(cast(ingested_at as timestamptz))
        from raw.{table}
    """).fetchone()

    if dernier is None:  # table vide : rien n'a été chargé
        print(f"raw.{table:<12} vide")
        problemes.append(f"{table} : aucune donnée chargée")
        continue

    age =datetime.now(timezone.utc) - dernier
    print(f"raw.{table:<12} {nb_lignes:>5} lignes | {nb_villes} villes | "
          f"dernier chargement il y a {age.total_seconds() / 3600:.1f} h")

    # 1. Fraîcheur : les données ont-elles été chargées récemment ?
    if age > MAX_AGE:
        problemes.append(f"{table} : données trop vieilles ({age})")
    # 2. Complétude : a-t-on bien toutes les villes ?
    if nb_villes < NB_VILLES:
        problemes.append(f"{table} : {nb_villes}/{NB_VILLES} villes seulement")

# 3. Complétude des mesures : part des valeurs PM2.5 manquantes
manquants = con.execute(
    "select avg(case when pm2_5 is null then 1.0 else 0 end) from raw.air_quality"
).fetchone()[0]
print(f"PM2.5 manquants : {manquants:.1%}")
if manquants > 0.2:
    problemes.append(f"trop de PM2.5 manquants ({manquants:.0%})")

if problemes:
    print("\n❌ PROBLÈMES DÉTECTÉS :")
    for p in problemes:
        print(f"  - {p}")
    sys.exit(1)
print("\n✅ Données fraîches et complètes")
