import os
import re
from pathlib import Path

import pandas as pd
import polars as pl

# --- CONFIGURACIÓN ---
PROJECT_DIR = Path(r"C:\Users\brian\Documents\Proyectos_IA")
TARGET_DIR = PROJECT_DIR / "data_raw"
OUTPUT_FILE = PROJECT_DIR / "REPORTE_AUDITORIA.txt"

# Limpiamos el reporte anterior si existe
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("=== REPORTE DE AUDITORÍA DE DATOS ===\n\n")


def strip_ansi(text):
    # Elimina los códigos de color para que el TXT sea legible
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_escape.sub("", text)


def log(msg, color="WHITE"):
    colors = {
        "CYAN": "\033[96m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "RED": "\033[91m",
        "RESET": "\033[0m",
        "WHITE": "\033[0m",
        "MAGENTA": "\033[95m",
    }

    # 1. Imprimir en Terminal (Con Colores)
    print(f"{colors.get(color, '')}{msg}{colors['RESET']}")

    # 2. Guardar en Archivo (Texto Plano Limpio)
    clean_msg = strip_ansi(str(msg))
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(clean_msg + "\n")


def analyze_csv(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            sample = f.read(4096)
            if not sample:
                return "VACIO", None

            count_semi = sample.count(";")
            count_comma = sample.count(",")
            count_tab = sample.count("\t")
            count_pipe = sample.count("|")

            if count_semi > count_comma and count_semi > count_tab:
                sep = ";"
            elif count_tab > count_comma:
                sep = "\t"
            elif count_pipe > count_comma:
                sep = "|"
            else:
                sep = ","

        df = pd.read_csv(
            filepath, sep=sep, nrows=1, encoding="utf-8", on_bad_lines="skip"
        )
        cols = list(df.columns)

        log(f"   [CSV] Sep: '{sep}' | Cols: {len(cols)}", "GREEN")
        log(f"   Variables: {cols[:5]} ...", "CYAN")
    except Exception as e:
        log(f"   [ERROR LECTURA CSV] {e}", "RED")


def analyze_parquet(filepath):
    try:
        lf = pl.scan_parquet(filepath)
        cols = list(lf.collect_schema().names())
        log(f"   [PARQUET] Motor Polars | Cols: {len(cols)}", "MAGENTA")
        log(f"   Variables: {cols[:5]} ...", "CYAN")
    except Exception as e:
        log(f"   [ERROR PARQUET] {e}", "RED")


def analyze_excel(filepath):
    try:
        xls = pd.ExcelFile(filepath)
        log(f"   [EXCEL] Hojas: {xls.sheet_names}", "YELLOW")
    except Exception as e:
        log(f"   [ERROR EXCEL] {e}", "RED")


print(f"\n🔬 BARRIDO ESPECTRAL -> GUARDANDO EN: {OUTPUT_FILE.name}")

if not TARGET_DIR.exists():
    log("¡CRÍTICO! La carpeta data_raw no existe.", "RED")
    exit()

file_count = 0
for root, dirs, files in os.walk(TARGET_DIR):
    for filename in files:
        filepath = Path(root) / filename

        if filename.startswith(".") or filename.endswith((".rar", ".zip", ".log")):
            continue

        size_mb = filepath.stat().st_size / (1024 * 1024)
        rel_path = filepath.relative_to(TARGET_DIR)

        log("-" * 60)
        log(f"📄 {rel_path} ({size_mb:.2f} MB)")

        ext = filepath.suffix.lower()
        if ext == ".csv":
            analyze_csv(filepath)
        elif ext == ".parquet":
            analyze_parquet(filepath)
        elif ext in [".xls", ".xlsx"]:
            analyze_excel(filepath)
        else:
            log("   [OTRO] Formato no analizado.", "YELLOW")

        file_count += 1

log(f"\n🏁 BARRIDO FINALIZADO. Archivos analizados: {file_count}")
print(f"\n✅ REPORTE GENERADO EXITOSAMENTE: {OUTPUT_FILE}")
