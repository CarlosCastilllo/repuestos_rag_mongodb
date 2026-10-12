# Guía para instalar y ejecutar el proyecto

Este tutorial configura el entorno local, conecta el proyecto con MongoDB Atlas,
inicializa las colecciones y ejecuta las pruebas disponibles. Los comandos están
escritos para Windows PowerShell.

## 1. Requisitos

- Python 3.10 o superior.
- Git.
- Un clúster de MongoDB Atlas y una base de datos a la que tu usuario tenga acceso.
- La dirección IP de tu computador permitida en **Atlas → Network Access**.

Este proyecto prepara la base de datos y realiza búsquedas vectoriales. Por ahora
no incluye una API ni un modelo LLM que redacte respuestas conversacionales.

## 2. Descargar el proyecto

Clona el repositorio y entra en su carpeta. Reemplaza la dirección por la URL del
repositorio de tu grupo:

```powershell
git clone <URL_DEL_REPOSITORIO>
cd repuestos-rag-mongodb
```

Si ya tienes el proyecto descargado, abre PowerShell en la carpeta `rag-mongodb`
y continúa con el paso siguiente.

## 3. Crear el entorno e instalar dependencias

Ejecuta estos comandos desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Cuando el entorno esté activo, PowerShell mostrará `(.venv)` al inicio de la
línea. Si Windows bloquea la activación, puedes continuar sin activarlo usando
`.\.venv\Scripts\python.exe -m pip install -r requirements.txt` y anteponiendo
`.\.venv\Scripts\python.exe` a los comandos Python de esta guía.

## 4. Configurar MongoDB Atlas

En Atlas, crea o selecciona un clúster, crea un usuario de base de datos y agrega
tu IP en **Network Access**. Copia la cadena de conexión del clúster, pero no la
compartas ni la publiques.

Crea tu archivo local `.env` a partir de la plantilla:

```powershell
Copy-Item .env.example .env
notepad .env
```

Reemplaza los marcadores de `MONGODB_URI` con el usuario, contraseña y nombre
reales del clúster. Conserva `MONGODB_DB_NAME=repuestos_rag` o usa el nombre de
base acordado por el grupo. Guarda el archivo y cierra el editor.

El `.env` contiene credenciales: **no lo subas a Git ni lo envíes por chat**.
Sube o comparte `.env.example`, que solo contiene marcadores.

## 5. Comprobar la conexión

```powershell
python -m scripts.test_connection
```

El resultado esperado termina con `Conexión verificada correctamente` y el nombre
de la base. El script inserta, lee y elimina un documento temporal en
`_test_connection`; no carga datos en las colecciones del proyecto.

## 6. Crear colecciones, reglas e índices

```powershell
python -m scripts.init_db
```

El inicializador crea las colecciones, aplica sus validaciones e índices normales
y solicita los índices vectoriales de Atlas. Puede ejecutarse más de una vez.
Atlas puede tardar en completar la construcción de los índices vectoriales.

> **Base ya creada con una versión anterior:** si `documentos`, `chunks` o
> `imagenes` contienen información, no ejecutes la migración. El script de
> migración se detiene para proteger esas colecciones si encuentra documentos.
> Si están vacías y todavía tienen los índices antiguos, ejecuta
> `python -m scripts.migrate_pdf_schema`; este retira los índices anteriores y
> vuelve a inicializar con el esquema alineado a la plantilla PDF.

## 7. Verificar colecciones e índices

```powershell
python -m scripts.verify_db
```

Comprueba que aparezcan las 15 colecciones con reglas, sus índices normales y,
para `chunks` e `imagenes`, los índices vectoriales con `estado=READY` y
`consultable=True`. Si todavía están construyéndose, espera un poco y vuelve a
ejecutar este comando.

## 8. Ejecutar las pruebas funcionales

Las pruebas son independientes; puedes ejecutarlas y guardar sus salidas por
separado:

```powershell
python -m scripts.test_validation
python -m scripts.test_vector_search
```

La primera comprueba que las reglas rechacen documentos incorrectos, acepten
documentos válidos y que una categoría duplicada sea bloqueada por el índice
único. La segunda inserta tres chunks sintéticos, ejecuta una búsqueda
`$vectorSearch` con filtros y luego elimina sus datos temporales. No ejecutes la
segunda hasta que el índice vectorial de `chunks` figure como listo.

Al terminar, ejecuta nuevamente:

```powershell
python -m scripts.verify_db
```

Confirma que las colecciones de prueba vuelvan a tener cero documentos. Si una
prueba informa que no pudo limpiar sus datos, revisa Atlas antes de repetirla.

## 9. Qué demuestra esta etapa

Esta configuración demuestra que la aplicación se conecta a Atlas, valida
documentos, aplica índices y recupera fragmentos similares por búsqueda
vectorial. La generación de respuestas redactadas requiere integrar después un
LLM y construir el flujo RAG completo.
