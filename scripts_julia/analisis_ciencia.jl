using LibPQ, DataFrames, CSV

println("🚀 EXTRAYENDO DATOS AGREGADOS PARA ANÁLISIS...")

conn = LibPQ.Connection("dbname=postgres user=postgres host=localhost")

# Agregamos por MES y JURISDICCIÓN (Mucho más liviano que día a día)
query = """
    SELECT 
        to_char(fecha_aplicacion, 'YYYY-MM-01')::date as fecha,
        jurisdiccion_aplicacion as provincia,
        count(*) as dosis
    FROM raw_nomivac
    WHERE fecha_aplicacion IS NOT NULL
    GROUP BY 1, 2
    ORDER BY 1, 2;
"""

result = execute(conn, query)
df = DataFrame(result)
close(conn)

# Guardamos el resultado procesado (serán unas pocas miles de filas, no millones)
output_path = "C:/Users/brian/Documents/Proyectos_IA/procesados_vacunas_mensual.csv"
CSV.write(output_path, df)

println("✅ Archivo guardado: ", output_path)
println("📊 Filas generadas: ", size(df, 1))