"""Validation des données reçues contre les contrats YAML (dossier contracts/).

Si un enregistrement viole le contrat, on lève ContractViolation :
le pipeline s'arrête AVANT de charger quoi que ce soit dans l'entrepôt.
"""
from pathlib import Path

import yaml

CONTRACTS_DIR = Path(__file__).resolve().parent.parent / "contracts"
TYPES = {"str": str, "float": (int, float)}


class ContractViolation(Exception):
    pass


def load_contract(name: str) -> dict:
    with open(CONTRACTS_DIR / f"{name}.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate(records: list[dict], contract: dict) -> None:
    errors = []
    columns = contract["columns"]
    seen_keys = set()

    for i, rec in enumerate(records):
        # 1. Colonnes inattendues (l'API a changé de format ?)
        extra = set(rec) - set(columns)
        if extra:
            errors.append(f"ligne {i}: colonnes hors contrat {sorted(extra)}")

        for col, rule in columns.items():
            value = rec.get(col)
            if value is None:
                if rule.get("required"):
                    errors.append(f"ligne {i}: '{col}' obligatoire mais absent")
                continue
            if not isinstance(value, TYPES[rule["type"]]):
                errors.append(f"ligne {i}: '{col}' type {type(value).__name__}, attendu {rule['type']}")
                continue
            if "min" in rule and value < rule["min"]:
                errors.append(f"ligne {i}: '{col}'={value} < min {rule['min']}")
            if "max" in rule and value > rule["max"]:
                errors.append(f"ligne {i}: '{col}'={value} > max {rule['max']}")

        # 2. Unicité de la clé primaire dans le lot
        key = tuple(rec.get(k) for k in contract["primary_key"])
        if key in seen_keys:
            errors.append(f"ligne {i}: clé dupliquée {key}")
        seen_keys.add(key)

    if errors:
        preview = "\n".join(errors[:10])
        raise ContractViolation(
            f"Contrat '{contract['source']}' v{contract['version']} violé "
            f"({len(errors)} erreurs) :\n{preview}"
        )
