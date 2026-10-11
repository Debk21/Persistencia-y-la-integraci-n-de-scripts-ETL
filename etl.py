import sqlite3
from pathlib import Path

import pandas as pd

#Configuracion de rutas
BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_CSV = BASE_DIR / "datos" / "ventas.csv"
ARCHIVO_SQL = BASE_DIR / "esquema.sql"
BASE_DATOS = BASE_DIR / "ventas.db"

#Extraccion de datos
def extraer_datos():
    """Lee los datos desde el archivo CSV."""
    print("Extrayendo datos...")

    if not ARCHIVO_CSV.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ARCHIVO_CSV}"
        )
    return pd.read_csv(ARCHIVO_CSV)

#Limpieza y transformacion de datos
def transformar_datos(df):
    """Limpia los datos y calcula el importe total"""
    print("Transformando datos...")

    columnas_requeridas = [
        "id_venta",
        "producto",
        "cantidad",
        "precio_unitario",
        "fecha",
    ]

    if not all(col in df.columns for col in columnas_requeridas):
        raise ValueError("El CSV no contiene todas las columnas requeridas.")   

    df = df[columnas_requeridas].copy()

    df["producto"] = df["producto"].astype("string").str.strip()
    df["fecha"] = df["fecha"].astype("string").str.strip()

    for columna in ["id_venta", "cantidad", "precio_unitario"]:
        df[columna] = pd.to_numeric(df[columna], errors="coerce")   

    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    df = df.dropna()
    df = df[
        (df["id_venta"] > 0)
        & (df["cantidad"] > 0)
        & (df["precio_unitario"] > 0)
        & (df["producto"].str.len() > 0)
    ]

    df = df.drop_duplicates(subset=["id_venta"], keep="last")

    df["id_venta"] = df["id_venta"].astype(int)
    df["cantidad"] = df["cantidad"].astype(int)
    df["precio_unitario"] = df["precio_unitario"].round(2)
    df["importe_total"] = (
        df["cantidad"] * df["precio_unitario"]
    ).round(2)
    df["fecha"] = df["fecha"].dt.strftime("%Y-%m-%d")

    print(f"Registros Validos: {len(df)}")

    return df[
        [
            "id_venta",
            "producto",
            "cantidad",
            "precio_unitario",
            "importe_total",
            "fecha"
        ]
    ]

#Carga y persistencia en SQLite
def cargar_datos(df):
    """Carga los datos en SQLite sin duplicar identificadores."""
    print("Cargando datos en SQLite...")

    conexion = sqlite3.connect(BASE_DATOS)

    try: 
        with conexion:
            esquema = ARCHIVO_SQL.read_text(encoding="utf-8")
            conexion.executescript(esquema)

            conexion.executemany(
                """
                INSERT INTO ventas (
                    id_venta,
                    producto,
                    cantidad,
                    precio_unitario,
                    importe_total,
                    fecha
                ) 
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id_venta) DO UPDATE SET
                    producto=excluded.producto,
                    cantidad=excluded.cantidad,
                    precio_unitario=excluded.precio_unitario,
                    importe_total=excluded.importe_total,
                    fecha=excluded.fecha
                    """,
                    df.itertuples(index=False, name=None),
            )
        print(f"Base de datos acutalizada: {BASE_DATOS.name}")

    finally:
        conexion.close()

#Ejecucion del proceso ETL
def main ():
    """Ejectura el flujo ETL completo"""
    try:
        datos = extraer_datos()
        datos_limpios = transformar_datos(datos)
        cargar_datos(datos_limpios)
        print("Proceso ETL finalizado correctamente")

    except (FileNotFoundError, ValueError, sqlite3.Error) as error:
        print(f"Error durante el proceso ETL: {error}")

    except Exception as error:
        print (f"Error inesperado: {error}")


if __name__ == "__main__":
    main()

    