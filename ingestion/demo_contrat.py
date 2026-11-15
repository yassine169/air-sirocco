"""Démo pour la présentation : le contrat bloque une donnée fausse.

Lancer avec : python -m ingestion.demo_contrat
"""
from ingestion.contracts import ContractViolation, load_contract, validate

donnee_fausse = [{
    "city": "Tunis", "time": "2026-11-14T10:00",
    "pm2_5": -5.0,      # impossible : une pollution ne peut pas être négative
    "pm10": 30.0, "dust": 4.0, "nitrogen_dioxide": 8.0, "ozone": 60.0,
}]

try:
    validate(donnee_fausse, load_contract("air_quality"))
    print("Donnée acceptée")
except ContractViolation as erreur:
    print("🛑 Donnée BLOQUÉE avant d'entrer dans l'entrepôt :")
    print(erreur)
