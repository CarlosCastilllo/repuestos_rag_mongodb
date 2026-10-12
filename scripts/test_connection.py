"""Verifica la conexión y las operaciones básicas con MongoDB."""

import sys

from pymongo.errors import PyMongoError


def main() -> int:
    """Ejecuta una prueba temporal de conexión y CRUD."""
    db = None
    crear_prueba = False

    try:
        from app.services.db_service import get_db, ping

        db = get_db()

        print("1. Comprobando conexión con el clúster...")
        if not ping():
            raise ConnectionError("El servidor no respondió al ping.")
        print("   ✔ Ping correcto")

        if "_test_connection" in db.list_collection_names():
            raise RuntimeError(
                "Ya existe la colección temporal _test_connection; "
                "no se modificó para proteger sus datos."
            )

        print("2. Insertando documento temporal...")
        coleccion = db["_test_connection"]
        resultado = coleccion.insert_one({"prueba": "conexion"})
        crear_prueba = True
        print("   ✔ Documento insertado")

        print("3. Leyendo el documento temporal...")
        documento = coleccion.find_one({"_id": resultado.inserted_id})
        if documento is None:
            raise RuntimeError("No se encontró el documento insertado.")
        print("   ✔ Documento leído")

        print("4. Borrando el documento y la colección temporal...")
        coleccion.delete_one({"_id": resultado.inserted_id})
        db.drop_collection("_test_connection")
        crear_prueba = False
        print("   ✔ Datos temporales eliminados")

        print(f"✔ Conexión verificada correctamente. Base de datos: {db.name}")
        return 0
    except Exception as error:
        if db is not None and crear_prueba:
            try:
                db.drop_collection("_test_connection")
            except PyMongoError:
                print("No se pudo eliminar la colección temporal durante la limpieza.")

        print(
            f"Error al verificar la conexión ({type(error).__name__}). "
            "Causa probable: URI mal escrita, usuario o clave incorrectos, "
            "o IP no autorizada en Network Access de Atlas."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
