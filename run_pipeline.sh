#!/bin/sh
# Lance tout le pipeline, étape par étape. S'arrête à la première erreur.
set -e

echo "=== 1/3 Ingestion (Yassine) ==="
python -m ingestion.pipeline_openmeteo

echo "=== 2/3 Transformation + tests dbt (Youssef) ==="
cd dbt_project
dbt seed --profiles-dir .
dbt build --profiles-dir .
cd ..

echo "=== 3/3 Santé des données (Nadia) ==="
if [ -f scripts/check_data.py ]; then
  python scripts/check_data.py
else
  echo "(scripts/check_data.py pas encore ajouté : étape ignorée)"
fi

echo "=== Pipeline terminé avec succès ==="
