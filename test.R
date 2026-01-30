library(DoubleML)
library(mlr3)
library(mlr3learners)
library(ranger) # Para Random Forest rápido

# 1. Simular un dataset más grande para que el Ryzen trabaje
set.seed(42)
n <- 2000
p <- 15
x <- matrix(rnorm(n * p), ncol = p)
d <- x[,1] + x[,2] + rnorm(n)
y <- 0.7 * d + x[,1]^2 + sin(x[,3]) + rnorm(n)

data <- data.frame(y, d, x)
obj_data <- double_ml_data_from_data_frame(data, y_col = "y", d_cols = "d")

# 2. Configurar el "Bosque" para usar tus núcleos
# Ranger detectará automáticamente tus 32 hilos
l_rf <- lrn("regr.ranger", num.trees = 500, importance = "impurity")

# 3. Estimación con validación cruzada (Cross-fitting)
dml_plr <- DoubleMLPLR$new(obj_data, ml_l = l_rf, ml_m = l_rf, n_folds = 5)
print("Iniciando estimación pesada en Ryzen 9...")
dml_plr$fit()

print("--- RESULTADOS PhD ---")
print(dml_plr$summary())