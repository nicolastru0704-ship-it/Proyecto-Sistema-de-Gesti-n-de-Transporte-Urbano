import csv
from pathlib import Path
from typing import List, Dict
import pandas as pd

BASE_DIR = Path.cwd() / "data"
BASE_DIR.mkdir(exist_ok=True)

DRIVERS_CSV = BASE_DIR / "drivers.csv"
PASSENGERS_CSV = BASE_DIR / "passengers.csv"
ROUTES_CSV = BASE_DIR / "routes.csv"
TRIPS_CSV = BASE_DIR / "trips.csv"

def ensure_files_exist():
    if not DRIVERS_CSV.exists():
        with DRIVERS_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nombre", "documento", "licencia", "ganancias_acumuladas"])
            writer.writeheader()
    if not PASSENGERS_CSV.exists():
        with PASSENGERS_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "nombre", "documento", "correo"])
            writer.writeheader()
    if not ROUTES_CSV.exists():
        with ROUTES_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "origen", "destino", "horario", "tarifa_base", "conductor_asignado_id"])
            writer.writeheader()
    if not TRIPS_CSV.exists():
        with TRIPS_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "route_id", "driver_id", "date_time", "passengers_count", "fare_total"])
            writer.writeheader()

def read_csv_to_dicts(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_dicts_to_csv(path: Path, dicts: List[Dict], fieldnames: List[str]):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dicts)

def append_dict_to_csv(path: Path, row: Dict, fieldnames: List[str]):
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)

def load_trips_df():
    try:
        df = pd.read_csv(TRIPS_CSV, parse_dates=["date_time"])
        df["passengers_count"] = df["passengers_count"].astype(int)
        df["fare_total"] = df["fare_total"].astype(float)
        return df
    except Exception:
        return pd.DataFrame(columns=["id", "route_id", "driver_id", "date_time", "passengers_count", "fare_total"])
