import csv

from sqlalchemy import create_engine, text

# --- CONFIGURACIÓN ---
CSV_PATH = (
    r"C:\Users\brian\Documents\Proyectos_IA\data_raw\SISA\datos_nomivac_covid19.csv"
)
DB_URL = "postgresql://postgres@localhost:5432/postgres"


def sanitize_col_name(name):
    """Limpia nombres de columnas (quita espacios, mayúsculas, etc)"""
    return name.lower().strip().replace(" ", "_").replace(".", "").replace('"', "")


print("🚀 INICIANDO INGESTA AUTÓNOMA DE NOMIVAC (21 GB) 🚀")

try:
    # 1. LEER HEADERS (Para saber la estructura REAL)
    print(f"1️⃣  Escaneando cabecera de: {CSV_PATH}...")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)  # Solo lee la primera línea

    print(f"   -> Detectadas {len(headers)} columnas exactas.")

    # 2. GENERAR SQL DINÁMICO
    # Creamos todos como TEXT para evitar errores de tipo, luego se castean si hace falta.
    cols_sql = [f"{sanitize_col_name(col)} text" for col in headers]
    cols_str = ",\n    ".join(cols_sql)

    create_table_sql = f"""
    DROP TABLE IF EXISTS raw_nomivac;
    CREATE TABLE raw_nomivac (
        {cols_str}
    );
    """

    print("2️⃣  Reconstruyendo tabla en Postgres...")
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()
        print("   -> Tabla 'raw_nomivac' creada con la estructura perfecta.")

    # 3. EJECUTAR COPY (Directo al motor)
    print("3️⃣  Inyectando datos (Esto puede tomar 5-10 minutos)...")

    # Usamos psycopg2 raw connection para el copy_expert (es lo más rápido que existe)
    raw_conn = engine.raw_connection()
    cur = raw_conn.cursor()

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        # copy_expert permite usar el comando COPY nativo
        sql_copy = "COPY raw_nomivac FROM STDIN WITH CSV HEADER DELIMITER ','"
        cur.copy_expert(sql_copy, f)
        raw_conn.commit()

    print("\n✅ ¡ÉXITO! CARGA MASIVA COMPLETADA.")

    # Verificación
    with engine.connect() as conn:
        count = conn.execute(text("SELECT count(*) FROM raw_nomivac")).scalar()
        print(f"📊 Registros totales en base de datos: {count:,.0f}")

except Exception as e:
    print(f"\n❌ ERROR FATAL: {e}")
