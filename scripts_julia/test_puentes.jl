using LibPQ
using DataFrames

println("🌉 PROBANDO PUENTES DE DATOS (V2 - RUTAS ABSOLUTAS) 🌉")

# --- RUTAS DE EJECUTABLES ---
# Usamos raw"..." para que las barras invertidas de Windows no den problemas
PYTHON_EXE = raw"C:\Users\brian\Documents\Proyectos_IA\venv_ia\Scripts\python.exe"
R_EXE = raw"C:\Program Files\R\R-4.5.2\bin\x64\Rscript.exe"

# 1. PUENTE JULIA -> SQL
try
    println("\n1️⃣  Julia conectando al Búnker...")
    conn = LibPQ.Connection("dbname=postgres user=postgres host=localhost")
    # Traemos el conteo
    result = execute(conn, "SELECT count(*) FROM raw_nomivac;")
    df = DataFrame(result)
    println("   ✅ Conexión Exitosa. Registros en Búnker: ", df[1,1])
    close(conn)
catch e
    println("   ❌ Falló Julia: ", e)
end

# 2. PUENTE PYTHON -> SQL
println("\n2️⃣  Verificando Python (Venv)...")
try
    # Llamamos explícitamente al Python del entorno virtual
    run(`$PYTHON_EXE -c "import psycopg2; conn = psycopg2.connect('dbname=postgres user=postgres host=localhost'); print('   ✅ Python tiene acceso al motor SQL.')"`)
catch e
    println("   ❌ Falló Python: Asegúrate de que 'psycopg2' esté instalado en venv_ia.")
    println("      (Tip: corre 'pip install psycopg2' en la terminal si falla)")
end

# 3. PUENTE R -> SQL
println("\n3️⃣  Verificando R...")
r_code = """
library(DBI)
library(RPostgres)
tryCatch({
    con <- dbConnect(RPostgres::Postgres(), dbname='postgres', host='localhost', user='postgres')
    print('   ✅ R tiene acceso al motor SQL.')
}, error = function(e) {
    print(paste('   ❌ R falló:', e$message))
})
"""
try
    run(`$R_EXE -e $r_code`)
catch e
    println("   ❌ Falló la ejecución de R.")
end

println("\n🏁 TEST FINALIZADO")