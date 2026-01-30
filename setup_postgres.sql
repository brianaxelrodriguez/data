-- 1. GEOLOCALIZACI?N (Hotelling, Voronoi, Distancias)
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch; -- Para NLP (Levenshtein, Soundex)
CREATE EXTENSION IF NOT EXISTS pg_trgm;       -- Para b?squeda de texto (Trigramas)

-- 2. PARALELISMO
SET max_parallel_workers_per_gather = 8; -- Usar tu Ryzen 9

-- 3. VECTORES (Para RAG/LLMs - Si falla, requiere instalaci?n manual de pgvector)
DO C:\Users\brian\Documents\Proyectos_IA 
BEGIN 
    CREATE EXTENSION IF NOT EXISTS vector; 
EXCEPTION 
    WHEN undefined_file THEN 
        RAISE NOTICE 'ALERTA: pgvector no instalado. Instalar manualmente para RAG.'; 
END C:\Users\brian\Documents\Proyectos_IA;
