import pytest

from ingestion.contracts import ContractViolation, load_contract, validate

AIR = load_contract("air_quality")


def good_row(**overrides):
    row = {"city": "Tunis", "time": "2026-11-14T10:00", "pm2_5": 12.0,
           "pm10": 30.0, "dust": 5.0, "nitrogen_dioxide": 8.0, "ozone": 60.0}
    return {**row, **overrides}


def test_valid_batch_passes():
    validate([good_row(), good_row(time="2026-11-14T11:00")], AIR)


def test_nulls_allowed_for_measures():
    validate([good_row(pm2_5=None)], AIR)


def test_negative_value_is_blocked():
    with pytest.raises(ContractViolation, match="pm2_5"):
        validate([good_row(pm2_5=-3.0)], AIR)


def test_missing_required_column_is_blocked():
    with pytest.raises(ContractViolation, match="city"):
        validate([good_row(city=None)], AIR)


def test_unexpected_column_is_blocked():
    with pytest.raises(ContractViolation, match="hors contrat"):
        validate([good_row(new_field=1)], AIR)


def test_duplicate_key_is_blocked():
    with pytest.raises(ContractViolation, match="dupliquée"):
        validate([good_row(), good_row()], AIR)
