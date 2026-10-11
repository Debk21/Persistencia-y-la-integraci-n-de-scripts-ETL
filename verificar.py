import sqlite3
from pathlib import Path

#Ruta de la base de datos
BASE_DATOS = Path(__file__).resolve().parent / "ventas.db"

#Consulta de registros y deteccion de duplicados
with sqlite3.connect(BASE_DATOS) as conexion:
    total = conexion.execute(
        "SELECT COUNT(*) FROM ventas"
    ).fetchone()[0]

    duplicados = conexion.execute("""
        SELECT COUNT (*)
        FROM (
            SELECT id_venta
            FROM ventas
            GROUP BY id_venta
            HAVING COUNT(*) > 1
            )
    """).fetchone()[0]

    print(f"Total de ventas guardadas: {total}")
    print(f"Identificadores duplicados: {duplicados}")

    