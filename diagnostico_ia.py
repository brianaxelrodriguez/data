import sys

import psycopg2
from google import genai

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def test_final_final():
    print("--- 🔬 INTENTO DEFINITIVO ---")

    # 1. POSTGRES (Si pusiste 'trust', no fallará)
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="local_db",
            user="postgres",
            password="admin",  # O déjalo vacío si usas 'trust'
            port="5432",
        )
        print("✅ DATABASE: CONECTADO.")
        conn.close()
    except Exception as e:
        print(f"❌ DATABASE: {repr(e)}")

    # 2. GEMINI (Cambiando a Gemini 1.5 Flash-Latest)
    try:
        client = genai.Client(api_key="TU_API_KEY")
        # Cambiamos el nombre del modelo al identificador más genérico
        response = client.models.generate_content(
            model="gemini-1.5-flash-latest", contents="Hola"
        )
        print("✅ GEMINI: CONECTADO.")
    except Exception as e:
        print(f"❌ GEMINI: {e}")


test_final_final()
