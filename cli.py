import sys
from datetime import datetime
from .core import SistemaTransporte

def menu():
    s = SistemaTransporte()

    def op_crear_conductor():
        nombre = input("Nombre conductor: ").strip()
        documento = input("Documento: ").strip()
        licencia = input("Licencia: ").strip()
        c = s.crear_conductor(nombre, documento, licencia)
        print(f"Conductor creado: {c.id} - {c.nombre}")

    def op_crear_pasajero():
        nombre = input("Nombre pasajero: ").strip()
        documento = input("Documento: ").strip()
        correo = input("Correo (opcional): ").strip() or None
        p = s.crear_pasajero(nombre, documento, correo)
        print(f"Pasajero creado: {p.id} - {p.nombre}")

    def op_crear_ruta():
        origen = input("Origen: ").strip()
        destino = input("Destino: ").strip()
        horario = input("Horario (HH:MM): ").strip()
        tarifa = float(input("Tarifa base (valor por pasajero): ").strip())
        r = s.crear_ruta(origen, destino, horario, tarifa)
        print(f"Ruta creada: {r.id} - {r.origen} → {r.destino}")

    def op_asignar_conductor():
        print("Rutas disponibles:")
        s.listar_rutas()
        rid = input("Ingrese route_id a asignar: ").strip()
        print("Conductores disponibles:")
        s.listar_conductores()
        did = input("Ingrese conductor_id: ").strip()
        try:
            s.asignar_conductor_a_ruta(rid, did)
            print("Conductor asignado correctamente.")
        except Exception as e:
            print("Error:", e)

    def op_registrar_viaje():
        print("Rutas:")
        s.listar_rutas()
        rid = input("Route ID: ").strip()
        ruta = s.rutas.get(rid)
        if not ruta:
            print("Ruta no encontrada.")
            return
        if ruta.conductor_asignado_id:
            print(f"Conductor asignado: {s.conductores[ruta.conductor_asignado_id].nombre}")
            did = ruta.conductor_asignado_id
        else:
            print("No hay conductor asignado a esta ruta. Listado de conductores:")
            s.listar_conductores()
            did = input("Ingrese driver_id para el viaje: ").strip()
        pasajeros = int(input("Número de pasajeros en el viaje: ").strip())
        fecha_txt = input("Fecha y hora del viaje (YYYY-MM-DD HH:MM) - enter = ahora: ").strip()
        try:
            if fecha_txt:
                dt = datetime.fromisoformat(fecha_txt)
            else:
                dt = datetime.now()
        except Exception:
            dt = datetime.now()
        try:
            trip = s.registrar_viaje(rid, did, pasajeros, dt)
            print("Viaje registrado:", trip)
        except Exception as e:
            print("Error al registrar viaje:", e)

    def op_reporte():
        stats = s.reporte_estadisticas()
        if not stats:
            print("No hay viajes registrados aún.")
            return
        print("\n=== REPORTE DE ESTADÍSTICAS ===")
        print(f"Total viajes registrados: {stats['total_viajes']}")
        print(f"Ruta más usada: {stats['ruta_mas_usada']}")
        print(f"Promedio de pasajeros por viaje: {stats['promedio_pasajeros_por_viaje']:.2f}")
        print("\nGanancias por ruta:")
        for ruta_name, g in stats["ganancias_por_ruta"].items():
            print(f"  - {ruta_name}: ${g:.2f}")
        print("\nGanancias por conductor:")
        for driver_name, g in stats["ganancias_por_conductor"].items():
            print(f"  - {driver_name}: ${g:.2f}")
        print("\nOcupación promedio por ruta (pasajeros):")
        for ruta_name, oc in stats["ocupacion_promedio_por_ruta"].items():
            print(f"  - {ruta_name}: {oc:.2f}")
        print("==============================\n")

    def op_listar():
        print("\n--- Rutas ---")
        s.listar_rutas()
        print("\n--- Conductores ---")
        s.listar_conductores()
        print("\n--- Pasajeros ---")
        s.listar_pasajeros()

    actions = {
        "1": ("Crear conductor", op_crear_conductor),
        "2": ("Crear pasajero", op_crear_pasajero),
        "3": ("Crear ruta", op_crear_ruta),
        "4": ("Asignar conductor a ruta", op_asignar_conductor),
        "5": ("Registrar viaje", op_registrar_viaje),
        "6": ("Generar reporte de estadísticas", op_reporte),
        "7": ("Listar todo", op_listar),
        "0": ("Salir", None)
    }

    while True:
        print("\n=== SISTEMA TRANSPORTE URBANO ===")
        for k, (desc, _) in actions.items():
            print(f"{k}. {desc}")
        choice = input("Selecciona una opción: ").strip()
        if choice == "0":
            print("Saliendo... ¡hasta luego!")
            break
        action = actions.get(choice)
        if not action:
            print("Opción inválida.")
            continue
        _, func = action
        func()

if __name__ == "__main__":
    menu()
