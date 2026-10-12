"""Prueba una búsqueda vectorial de Atlas con chunks temporales."""

import sys
import time
from uuid import uuid4

from bson import ObjectId
from pymongo.errors import PyMongoError

from app.schemas.chunks import INDICE_VECTORIAL


def _crear_vector(valores: tuple[float, float]) -> list[float]:
    """Construye un vector de prueba con la dimensión configurada."""
    dimensiones = INDICE_VECTORIAL["definicion"]["fields"][0]["numDimensions"]
    return [*valores, *([0.0] * (dimensiones - len(valores)))]


def main() -> int:
    """Inserta, busca y limpia tres documentos sintéticos."""
    try:
        from app.services.db_service import get_db

        coleccion = get_db()["chunks"]
        indice = next(
            (
                elemento
                for elemento in coleccion.list_search_indexes()
                if elemento.get("name") == INDICE_VECTORIAL["nombre"]
            ),
            None,
        )
        if indice is None:
            raise RuntimeError(
                f"No existe el índice {INDICE_VECTORIAL['nombre']} en chunks."
            )
        if indice.get("status") != "READY" or indice.get("queryable") is not True:
            raise RuntimeError(
                f"El índice {INDICE_VECTORIAL['nombre']} aún no está listo "
                "para consultar."
            )
    except Exception as error:
        print(
            f"No se pudo preparar la búsqueda vectorial "
            f"({type(error).__name__}): {error}"
        )
        return 1

    idioma_prueba = f"prueba-{uuid4().hex}"
    documentos = [
        {
            "doc_id": ObjectId(),
            "chunk_index": indice,
            "estrategia_chunking": "fixed-size",
            "chunk_texto": f"Chunk sintético de prueba {indice}.",
            "embedding": _crear_vector(vector),
            "modelo": "prueba-temporal",
            "idioma": idioma_prueba,
        }
        for indice, vector in enumerate(((1.0, 0.0), (0.8, 0.6), (0.6, 0.8)))
    ]
    ids_insertados = []
    filtro_limpieza = {
        "idioma": idioma_prueba,
        "modelo": "prueba-temporal",
    }
    error_prueba = None
    error_limpieza = None

    try:
        for documento in documentos:
            resultado = coleccion.insert_one(documento)
            ids_insertados.append(resultado.inserted_id)
        print(f"[OK] Se insertaron {len(ids_insertados)} chunks temporales")

        pipeline = [
            {
                "$vectorSearch": {
                    "index": INDICE_VECTORIAL["nombre"],
                    "path": "embedding",
                    "queryVector": _crear_vector((1.0, 0.0)),
                    "numCandidates": 10,
                    "limit": 3,
                    "filter": {
                        "idioma": {"$eq": idioma_prueba},
                        "estrategia_chunking": {"$eq": "fixed-size"},
                    },
                }
            },
            {"$project": {"_id": 1, "score": {"$meta": "vectorSearchScore"}}},
        ]
        ids_encontrados = {
            resultado["_id"] for resultado in []
        }
        limite_espera = time.monotonic() + 60
        while not ids_encontrados and time.monotonic() < limite_espera:
            resultados = coleccion.aggregate(pipeline)
            ids_encontrados = {
                resultado["_id"]
                for resultado in resultados
                if resultado["_id"] in ids_insertados
            }
            if not ids_encontrados:
                time.sleep(5)

        if not ids_encontrados:
            raise AssertionError(
                "Atlas no devolvió los chunks de prueba dentro de 60 segundos. "
                "Confirma que el índice esté READY y vuelve a ejecutar la prueba."
            )
        print(
            f"[OK] $vectorSearch devolvió {len(ids_encontrados)} chunks de prueba "
            "con el filtro de idioma y estrategia"
        )
    except Exception as error:
        error_prueba = error
        print(f"[ERROR] Falló la búsqueda vectorial ({type(error).__name__}): {error}")
    finally:
        try:
            coleccion.delete_many(filtro_limpieza)
            print("[OK] Chunks temporales eliminados")
        except PyMongoError as error:
            error_limpieza = error
            print(
                "[ERROR] No se pudieron limpiar todos los chunks temporales "
                f"({type(error).__name__}): {error}"
            )

    if error_prueba is not None or error_limpieza is not None:
        return 1
    print("[OK] Prueba de búsqueda vectorial completada")
    return 0


if __name__ == "__main__":
    sys.exit(main())
