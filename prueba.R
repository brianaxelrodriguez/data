# --- CONFIGURACIÓN DE ENTORNO ---
# Forzamos la ruta de tus librerías PhD (por si el .Rprofile no cargó)
.libPaths(c("C:/Users/brian/Documents/Proyectos_IA/R_library", .libPaths()))

# Activamos el visor de gráficos de VSCode
options(vsc.plot = TRUE)

# --- CARGA DE LIBRERÍAS ---
library(dagitty)
library(ggdag)
library(ggplot2)
library(reticulate)

# Conectamos con tu Python
use_python("C:/Users/brian/Documents/Proyectos_IA/venv_ia/Scripts/python.exe", required = TRUE)

# --- 1. DEFINICIÓN DEL MODELO ---
dag_modelo <- dagitty('dag {
    Educacion [pos="0,0"]
    Salario [pos="2,0"]
    Habilidad [pos="1,1"]
    Habilidad -> Educacion
    Habilidad -> Salario
    Educacion -> Salario
}')

# --- 2. GRAFICAMOS ---
# Al ejecutar esta parte, VSCode debería abrir la pestaña "R Plot" automáticamente
p <- ggdag(dag_modelo, text_col = "white") +
    theme_dag() +
    scale_x_continuous(breaks = NULL, limits = c(-0.5, 2.5)) +
    scale_y_continuous(breaks = NULL, limits = c(-0.5, 1.5)) +
    labs(
        title = "Modelo de Inferencia Causal",
        subtitle = "Educación, Habilidad y Salario"
    )

print(p) # Forzamos la impresión del objeto gráfico

# --- 3. PRUEBA DE PYTHON ---
message("\n>>> Verificando conexión con Python...")
py_run_string("import numpy as np; print('Numpy listo en el venv, versión:', np.__version__)")
