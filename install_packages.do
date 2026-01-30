* --- DEFINIR RUTAS DE INSTALACI?N ---
sysdir set PLUS "C:\Users\brian\Documents\Proyectos_IA\stata_lib\plus"
sysdir set PERSONAL "C:\Users\brian\Documents\Proyectos_IA\stata_lib\personal"

* --- UTILIDADES B?SICAS ---
ssc install ftools, replace      // Faster Stata tools (Requisito para reghdfe)
ssc install gtools, replace      // Faster group operations (usa C plugins)

* --- ECONOMETR?A & INFERENCIA CAUSAL ---
ssc install reghdfe, replace     // Fixed Effects (Est?ndar de oro)
ssc install ivreg2, replace      // Variables instrumentales robustas
ssc install ranktest, replace    // Tests de rango para IV
ssc install estout, replace      // Exportar tablas a LaTeX/Excel
ssc install outreg2, replace     // Otra opci?n de exportaci?n
ssc install boottest, replace    // Wild Bootstrap (Inferencia robusta en small samples)
ssc install ritest, replace      // Randomization Inference
ssc install drdid, replace       // Doubly Robust Diff-in-Diff
ssc install csdid, replace       // Callaway & Sant'Anna DID (Heterogeneous treatment effects)

* --- SERIES DE TIEMPO / ESPACIAL ---
ssc install spmap, replace       // Mapas en Stata (b?sico, R/Python son mejores)
ssc install shp2dta, replace     // Convertir Shapefiles
ssc install xcorr, replace       // Cross-correlation
ssc install ardl, replace        // Autoregressive Distributed Lag

* --- MACHINE LEARNING (Lo que Stata puede hacer) ---
ssc install lassopack, replace   // LASSO, Ridge, Elastic Net (Regularization)
net install rforest, from("https://raw.githubusercontent.com/stevebez/rforest/master/") replace // Random Forest wrapper
ssc install svmachines, replace  // Support Vector Machines (b?sico)

* --- VISUALIZACI?N ---
ssc install scheme-pack, replace // Esquemas de color modernos (Unibe, Clean)
ssc install colorpalette, replace
ssc install grstyle, replace

exit, clear
