# Proyecto RAG con MongoDB

Base inicial para configurar la conexión y crear las colecciones vacías de una tienda de repuestos de motos.

## Configuración

Desde esta carpeta, crea y activa un entorno virtual e instala las dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copia `.env.example` a `.env` y completa `MONGODB_URI` con los datos de tu clúster de MongoDB Atlas. No compartas ni subas el archivo `.env`.

## Ejecución

Con el entorno configurado y una URI válida, verifica la conexión:

```powershell
python -m scripts.test_connection
```

Después crea las colecciones:

```powershell
python -m scripts.init_db
```

`init_db` se puede ejecutar varias veces; las colecciones existentes no se duplican.

## Alinear una base ya inicializada con la plantilla PDF

Si inicializaste anteriormente la base con el esquema previo, verifica primero que
`documentos`, `chunks` e `imagenes` no tengan datos. Luego ejecuta:

```powershell
python -m scripts.migrate_pdf_schema
```

El script se niega a retirar índices si encuentra documentos en esas colecciones.
Después de la migración, comprueba el estado con:

```powershell
python -m scripts.verify_db
```

Los índices vectoriales pueden tardar en quedar consultables; `verify_db` muestra
su estado y el valor de `queryable`.

Las pruebas prácticas de las reglas e índices únicos y de la búsqueda vectorial
son independientes. Ejecuta cada script por separado cuando quieras guardar su
salida como evidencia:

```powershell
python -m scripts.test_validation
python -m scripts.test_vector_search
```

Ambos scripts usan datos temporales y los eliminan al terminar.
