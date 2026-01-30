import os

import psycopg2
from dotenv import load_dotenv
from google import genai

# Cargar variables de entorno
load_dotenv()

# Variables
API_KEY = os.getenv("GOOGLE_API_KEY")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def ejecutar_laboratorio():
    conn = None
    try:
        print("--- INICIANDO SISTEMA ---")

        # 1. Conexion a Gemini (Usando el modelo 2.0 que ya vimos que tienes)
        client = genai.Client(api_key=API_KEY)

        # He puesto 2.0-flash porque es el mas probable que te suelte la cuota primero
        # Si sigue el error 429, solo hay que esperar a que Google habilite tu IP
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Genera un resumen de una linea sobre la importancia de la economia de la salud.",
        )
        respuesta_ia = response.text
        print("✅ Gemini conectado y respondiendo.")

        # 2. Conexion a PostgreSQL con codificacion forzada
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            client_encoding="utf8",  # Esto evita el error 0xab/0xf3
        )
        cur = conn.cursor()
        print("✅ PostgreSQL conectado correctamente.")

        # 3. Creacion de tabla y guardado de datos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS memoria_ia (
                id SERIAL PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                contenido TEXT
            );
        """)

        cur.execute("INSERT INTO memoria_ia (contenido) VALUES (%s)", (respuesta_ia,))
        conn.commit()

        print("\n--- RESULTADO FINAL ---")
        print(f"IA dice: {respuesta_ia}")
        print("💾 Datos guardados en la base de datos.")

        cur.close()

    except Exception as e:
        print("\n❌ ERROR EN EL SISTEMA:")
        print(e)

    finally:
        if conn is not None:
            conn.close()
            print("\n--- CONEXIONES CERRADAS ---")


if __name__ == "__main__":
    ejecutar_laboratorio()
