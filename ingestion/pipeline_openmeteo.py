"""Ingestion Open-Meteo (qualité de l'air + météo) vers DuckDB avec dlt.

- Aucune clé d'API nécessaire.
- write_disposition="merge" sur la clé (city, time) : relancer le pipeline
  met à jour les lignes existantes au lieu de créer des doublons.
"""
import csv
import os
from datetime import datetime, timezone
from pathlib import Path

import dlt
import requests

from ingestion.contracts import load_contract, validate

ROOT = Path(__file__).resolve().parent.parent
CITIES_CSV = ROOT / "dbt_project" / "seeds" / "cities.csv"
DUCKDB_PATH = os.getenv("DUCKDB_PATH", str(ROOT / "data" / "warehouse.duckdb"))

AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
AIR_VARS = ["pm2_5", "pm10", "dust", "nitrogen_dioxide", "ozone"]
WEATHER_VARS = ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "wind_direction_10m"]


def load_cities() -> list[dict]:
    with open(CITIES_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fetch_hourly(url: str, variables: list[str], city: dict, past_days: int) -> list[dict]:
    """Appelle l'API pour une ville et renvoie une ligne par heure."""
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "hourly": ",".join(variables),
        "past_days": past_days,
        "forecast_days": 1,
        "timezone": "Africa/Tunis",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    hourly = resp.json()["hourly"]
    return [
        {"city": city["city"], "time": t, **{v: hourly[v][i] for v in variables}}
        for i, t in enumerate(hourly["time"])
    ]


def collect(url, variables, contract_name, past_days):
    """Récupère toutes les villes, valide le contrat, puis ajoute ingested_at."""
    records = []
    for city in load_cities():
        records.extend(fetch_hourly(url, variables, city, past_days))
    validate(records, load_contract(contract_name))  # bloque si contrat violé
    now = datetime.now(timezone.utc).isoformat()
    return [{**r, "ingested_at": now} for r in records]


def run(past_days: int = 2) -> dict:
    air = collect(AIR_URL, AIR_VARS, "air_quality", past_days)
    weather = collect(WEATHER_URL, WEATHER_VARS, "weather", past_days)

    pipeline = dlt.pipeline(
        pipeline_name="air_sirocco",
        destination=dlt.destinations.duckdb(DUCKDB_PATH),
        dataset_name="raw",
    )
    info = pipeline.run(
        [
            dlt.resource(air, name="air_quality", primary_key=["city", "time"],
                         write_disposition="merge"),
            dlt.resource(weather, name="weather", primary_key=["city", "time"],
                         write_disposition="merge"),
        ]
    )
    print(info)
    # Petit contrôle : combien de lignes au total dans l'entrepôt ?
    with pipeline.sql_client() as client:
        for table in ("air_quality", "weather"):
            n = client.execute_sql(f"select count(*) from {table}")[0][0]
            print(f"raw.{table} : {n} lignes au total")
    return {"air_rows": len(air), "weather_rows": len(weather)}


if __name__ == "__main__":
    print(run())
