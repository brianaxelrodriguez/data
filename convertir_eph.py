import pandas as pd

# Rutas
input_path = r"C:\Users\brian\Documents\Proyectos_IA\data_raw\Procesados\EPH_Panel_Master.parquet"
output_path = input_path.replace(".parquet", ".csv")

print(f"📖 Leyendo Parquet: {input_path}")

# Leer el archivo (requiere pyarrow o fastparquet, que seguro ya tienes)
df = pd.read_parquet(input_path)

print(f"📊 Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"💾 Guardando CSV en: {output_path} ...")

# Guardar como CSV
# index=False para no agregar una columna extra de índices numéricos
# encoding='utf-8-sig' ayuda a que Excel reconozca bien los acentos
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("✅ ¡Listo! Conversión terminada.")
