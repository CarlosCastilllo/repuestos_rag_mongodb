"""Prueba validaciones e índices únicos con documentos temporales."""

import sys
from datetime import datetime, timezone
from uuid import uuid4

from bson import ObjectId
from pymongo.errors import DuplicateKeyError, OperationFailure


def _esperar_rechazo_validacion(coleccion, documento: dict, ids_prueba: dict) -> None:
    """Confirma que MongoDB rechace un documento por su regla de validación."""
    try:
        resultado = coleccion.insert_one(documento)
    except OperationFailure as error:
        if error.code != 121:
            raise
        print(f"  ✔ {coleccion.name}: documento inválido rechazado")
        return

    ids_prueba[coleccion.name].append(resultado.inserted_id)
    raise AssertionError(
        f"{coleccion.name}: MongoDB aceptó un documento que debía rechazar."
    )


def _insertar_valido(coleccion, documento: dict, ids_prueba: dict) -> None:
    resultado = coleccion.insert_one(documento)
    ids_prueba[coleccion.name].append(resultado.inserted_id)
    print(f"  ✔ {coleccion.name}: documento válido aceptado")


def main() -> int:
    """Ejecuta pruebas de rechazo, aceptación, unicidad y limpieza."""
    try:
        from app.services.db_service import get_db

        db = get_db()
        nombres = set(db.list_collection_names())
        requeridas = {"productos", "pedidos", "chunks", "imagenes", "categorias"}
        faltantes = requeridas - nombres
        if faltantes:
            raise RuntimeError(
                "Faltan colecciones necesarias: " + ", ".join(sorted(faltantes))
            )
    except Exception as error:
        print(
            f"No se pudieron preparar las pruebas ({type(error).__name__}). "
            "Revisa la conexión y que las colecciones estén inicializadas."
        )
        return 1

    colecciones = {nombre: db[nombre] for nombre in requeridas}
    ids_prueba = {nombre: [] for nombre in requeridas}
    fecha = datetime.now(timezone.utc)
    identificador = uuid4().hex[:12]
    referencia = ObjectId()
    producto_valido = {
        "nombre": f"Prueba temporal {identificador}",
        "categoria": {"_id": ObjectId(), "nombre": "Prueba temporal"},
        "marca": {"_id": ObjectId(), "nombre": "Prueba temporal"},
        "precio": 100,
        "stock": 1,
        "especificaciones": {},
    }
    chunk_valido = {
        "doc_id": referencia,
        "chunk_index": 0,
        "estrategia_chunking": "fixed-size",
        "chunk_texto": "Fragmento temporal para probar la validación.",
        "embedding": [0.0] * 384,
        "modelo": "prueba-temporal",
    }
    imagen_valida = {
        "doc_id": referencia,
        "ruta_archivo": f"prueba-temporal-{identificador}.jpg",
        "descripcion": "Imagen temporal para probar la validación.",
        "etiquetas": ["prueba"],
        "embedding": [0.0] * 512,
        "modelo": "prueba-temporal",
    }

    print("Probando rechazos de validación...")
    try:
        producto_invalido = {**producto_valido, "precio": 0}
        _esperar_rechazo_validacion(
            colecciones["productos"], producto_invalido, ids_prueba
        )

        pedido_sin_items = {
            "cliente_id": ObjectId(),
            "vendedor": "prueba temporal",
            "canal": "mostrador",
            "fecha": fecha,
            "items": [],
            "total": 0,
        }
        _esperar_rechazo_validacion(
            colecciones["pedidos"], pedido_sin_items, ids_prueba
        )

        chunk_invalido = {**chunk_valido, "embedding": [0.0] * 300}
        _esperar_rechazo_validacion(
            colecciones["chunks"], chunk_invalido, ids_prueba
        )

        print("Probando aceptación de documentos válidos...")
        _insertar_valido(
            colecciones["productos"], producto_valido, ids_prueba
        )
        _insertar_valido(colecciones["chunks"], chunk_valido, ids_prueba)
        _insertar_valido(colecciones["imagenes"], imagen_valida, ids_prueba)

        print("Probando el índice único de categorías...")
        categoria = {"nombre": f"prueba-{identificador}"}
        _insertar_valido(colecciones["categorias"], categoria, ids_prueba)
        try:
            duplicado = colecciones["categorias"].insert_one(categoria)
        except DuplicateKeyError:
            print("  ✔ categorias: el índice único rechazó el duplicado")
        else:
            ids_prueba["categorias"].append(duplicado.inserted_id)
            raise AssertionError(
                "categorias: el índice único aceptó un nombre duplicado."
            )
    except Exception as error:
        print(f"✘ Prueba fallida ({type(error).__name__}): {error}")
        return 1
    finally:
        errores_limpieza = []
        for nombre, ids in ids_prueba.items():
            if ids:
                try:
                    colecciones[nombre].delete_many({"_id": {"$in": ids}})
                except Exception as error:
                    errores_limpieza.append(
                        f"{nombre} ({type(error).__name__})"
                    )
        if errores_limpieza:
            print(
                "✘ No se pudieron limpiar todos los datos temporales: "
                + ", ".join(errores_limpieza)
            )
        else:
            print("✔ Datos de prueba eliminados")

    if errores_limpieza:
        return 1
    print("✔ Pruebas de reglas e índice único completadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
