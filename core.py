from datetime import datetime
from typing import Dict, Optional
from .models.conductor import Conductor
from .models.pasajero import Pasajero
from .models.ruta import Ruta
from .storage.csv_store import (
    ensure_files_exist, read_csv_to_dicts, write_dicts_to_csv,
    append_dict_to_csv, load_trips_df,
    DRIVERS_CSV, PASSENGERS_CSV, ROUTES_CSV, TRIPS_CSV
)

class SistemaTransporte:
    def __init__(self):
        ensure_files_exist()
        self.conductores: Dict[str, Conductor] = {}
        self.pasajeros: Dict[str, Pasajero] = {}
        self.rutas: Dict[str, Ruta] = {}
        self.load_all()

    def load_all(self):
        # Conductores
        rows = read_csv_to_dicts(DRIVERS_CSV)
        for row in rows:
            c = Conductor(row["nombre"], row["documento"], row["licencia"])
            c.id = row["id"]
            try:
                c.ganancias_acumuladas = float(row.get("ganancias_acumuladas", 0.0))
            except:
                c.ganancias_acumuladas = 0.0
            self.conductores[c.id] = c

        # Pasajeros
        rows = read_csv_to_dicts(PASSENGERS_CSV)
        for row in rows:
            p = Pasajero(row["nombre"], row["documento"], row.get("correo"))
            p.id = row["id"]
            self.pasajeros[p.id] = p

        # Rutas
        rows = read_csv_to_dicts(ROUTES_CSV)
        for row in rows:
            r = Ruta(row["origen"], row["destino"], row["horario"], float(row["tarifa_base"]))
            r.id = row["id"]
            r.conductor_asignado_id = row.get("conductor_asignado_id") or None
            self.rutas[r.id] = r

    # Save helpers
    def _save_conductores(self):
        dicts = [c.to_dict() for c in self.conductores.values()]
        write_dicts_to_csv(DRIVERS_CSV, dicts, ["id", "nombre", "documento", "licencia", "ganancias_acumuladas"])

    def _save_pasajeros(self):
        dicts = [p.to_dict() for p in self.pasajeros.values()]
        write_dicts_to_csv(PASSENGERS_CSV, dicts, ["id", "nombre", "documento", "correo"])

    def _save_rutas(self):
        dicts = [r.to_dict() for r in self.rutas.values()]
        write_dicts_to_csv(ROUTES_CSV, dicts, ["id", "origen", "destino", "horario", "tarifa_base", "conductor_asignado_id"])

    # CRUD
    def crear_conductor(self, nombre: str, documento: str, licencia: str) -> Conductor:
        c = Conductor(nombre, documento, licencia)
        self.conductores[c.id] = c
        self._save_conductores()
        return c

    def crear_pasajero(self, nombre: str, documento: str, correo: Optional[str] = None) -> Pasajero:
        p = Pasajero(nombre, documento, correo)
        self.pasajeros[p.id] = p
        self._save_pasajeros()
        return p

    def crear_ruta(self, origen: str, destino: str, horario: str, tarifa_base: float) -> Ruta:
        r = Ruta(origen, destino, horario, tarifa_base)
        self.rutas[r.id] = r
        self._save_rutas()
        return r

    def asignar_conductor_a_ruta(self, route_id: str, conductor_id: str):
        if route_id not in self.rutas:
            raise ValueError("Ruta no existe")
        if conductor_id not in self.conductores:
            raise ValueError("Conductor no existe")
        self.rutas[route_id].asignar_conductor(conductor_id)
        self._save_rutas()

    def registrar_viaje(self, route_id: str, driver_id: str, passengers_count: int, date_time: Optional[datetime] = None):
        if route_id not in self.rutas:
            raise ValueError("Ruta no encontrada")
        if driver_id not in self.conductores:
            raise ValueError("Conductor no encontrado")
        date_time = date_time or datetime.now()
        tarifa = self.rutas[route_id].tarifa_base
        fare_total = tarifa * passengers_count
        row = {
            "id": __import__("uuid").uuid4().hex,
            "route_id": route_id,
            "driver_id": driver_id,
            "date_time": date_time.isoformat(),
            "passengers_count": int(passengers_count),
            "fare_total": float(fare_total)
        }
        append_dict_to_csv(TRIPS_CSV, row, ["id", "route_id", "driver_id", "date_time", "passengers_count", "fare_total"])
        # actualizar cache conductor
        self.conductores[driver_id].ganancias_acumuladas += fare_total
        self._save_conductores()
        return row

    # Estadísticas
    def reporte_estadisticas(self):
        df = load_trips_df()
        if df.empty:
            return {}
        total_viajes = len(df)
        ruta_uso = df["route_id"].value_counts()
        ruta_mas_usada_id = ruta_uso.idxmax()
        ruta_mas_usada_count = int(ruta_uso.max())
        promedio_pasajeros = float(df["passengers_count"].mean())
        ganancias_ruta = df.groupby("route_id")["fare_total"].sum().to_dict()
        ganancias_por_ruta = {}
        for rid, g in ganancias_ruta.items():
            r = self.rutas.get(rid)
            name = f"{r.origen} → {r.destino}" if r else rid
            ganancias_por_ruta[name] = float(g)
        ganancias_driver = df.groupby("driver_id")["fare_total"].sum().to_dict()
        ganancias_por_conductor = {}
        for did, g in ganancias_driver.items():
            d = self.conductores.get(did)
            name = d.nombre if d else did
            ganancias_por_conductor[name] = float(g)
        ocupacion = df.groupby("route_id")["passengers_count"].mean().to_dict()
        ocupacion_por_ruta = {}
        for rid, oc in ocupacion.items():
            r = self.rutas.get(rid)
            name = f"{r.origen} → {r.destino}" if r else rid
            ocupacion_por_ruta[name] = float(oc)
        ruta_mas_usada_name = None
        if ruta_mas_usada_id in self.rutas:
            r = self.rutas[ruta_mas_usada_id]
            ruta_mas_usada_name = f"{r.origen} → {r.destino} (veces: {ruta_mas_usada_count})"
        return {
            "total_viajes": total_viajes,
            "ruta_mas_usada": ruta_mas_usada_name,
            "promedio_pasajeros_por_viaje": promedio_pasajeros,
            "ganancias_por_ruta": ganancias_por_ruta,
            "ganancias_por_conductor": ganancias_por_conductor,
            "ocupacion_promedio_por_ruta": ocupacion_por_ruta
        }

