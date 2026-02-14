import time

from sqlalchemy import create_engine, text

# --- CONFIGURACIÓN ---
DB_URL = "postgresql://postgres@localhost:5432/postgres"


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


print("🚀 INICIANDO REFINERÍA DE DATOS (NOMIVAC 119M) 🚀")
print("⚠️  Advertencia: Esta operación reescribe la tabla. Puede tardar 10-20 mins.")

try:
    engine = create_engine(DB_URL, isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        # 1. CONVERTIR FECHAS (De Texto a DATE real)
        # Esto permite hacer: WHERE fecha > '2021-01-01' en milisegundos
        log("1️⃣  Convirtiendo columna 'fecha_aplicacion' a tipo DATE...")
        conn.execute(
            text("""
            ALTER TABLE raw_nomivac 
            ALTER COLUMN fecha_aplicacion TYPE DATE 
            USING NULLIF(fecha_aplicacion, '')::DATE;
        """)
        )
        log("   ✅ Fechas optimizadas.")

        # 2. CONVERTIR NÚMEROS (De Texto a INTEGER/SMALLINT)
        # Ahorra espacio (RAM y Disco) y acelera sumas/conteos
        log("2️⃣  Convirtiendo dosis y códigos a números...")
        conn.execute(
            text("""
            ALTER TABLE raw_nomivac 
            ALTER COLUMN orden_dosis TYPE SMALLINT 
            USING NULLIF(orden_dosis, '')::SMALLINT;
            
            ALTER TABLE raw_nomivac 
            ALTER COLUMN cod_dosis_generica TYPE SMALLINT 
            USING NULLIF(cod_dosis_generica, '')::SMALLINT;
        """)
        )
        log("   ✅ Números optimizados.")

        # 3. CREAR ÍNDICES (La clave de la velocidad)
        # Índice Geo-Temporal: Para filtrar por Provincia y Fecha a la vez
        log("3️⃣  Creando Súper-Índice (Jurisdicción + Fecha)... (Paciencia)")
        conn.execute(
            text("""
            CREATE INDEX IF NOT EXISTS idx_nomivac_geo_fecha 
            ON raw_nomivac (jurisdiccion_aplicacion, fecha_aplicacion);
        """)
        )

        # Índice por Vacuna: Para separar Sputnik, Astrazeneca, etc.
        log("4️⃣  Creando Índice de Vacunas...")
        conn.execute(
            text("""
            CREATE INDEX IF NOT EXISTS idx_nomivac_vacuna 
            ON raw_nomivac (vacuna);
        """)
        )

        # Índice ID Persona (Hasheado): Para contar personas únicas
        log("5️⃣  Creando Índice de Personas (Hash)...")
        conn.execute(
            text("""
            CREATE INDEX IF NOT EXISTS idx_nomivac_persona 
            ON raw_nomivac (id_persona_hash);
        """)
        )
        log("   ✅ Índices construidos.")

        # 4. MANTENIMIENTO FINAL
        log("6️⃣  Ejecutando VACUUM ANALYZE (Actualizando estadísticas del motor)...")
        conn.execute(text("VACUUM ANALYZE raw_nomivac;"))

    print("\n🏁 ¡OPTIMIZACIÓN COMPLETADA! TU BÚNKER ESTÁ LISTO.")
    print("   Ahora puedes hacer consultas de Big Data en tiempo real.")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
