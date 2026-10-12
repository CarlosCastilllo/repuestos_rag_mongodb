"""Migra los índices existentes al esquema práctico de la plantilla PDF."""

import sys

from pymongo.errors import PyMongoError

COLECCIONES_AFECTADAS = ("documentos", "chunks", "imagenes")
INDICES_NORMALES_OBSOLETOS = {
    "documentos": ("txt_titulo_contenido",),
    "chunks": ("idx_estrategia_idioma_categoria",),
    "imagenes": ("idx_producto", "idx_documento"),
}
INDICES_VECTORIALES_OBSOLETOS = {
    "chunks": "vector_chunks",
    "imagenes": "vector_imagenes",
}


def main() -> int:
    """Retira índices incompatibles y ejecuta el inicializador actualizado."""
    try:
        from app.services.db_service import get_db

        db = get_db()
        existentes = set(db.list_collection_names())
        faltantes = set(COLECCIONES_AFECTADAS) - existentes
        if faltantes:
            print(
                "No se inició la migración; faltan colecciones: "
                + ", ".join(sorted(faltantes))
            )
            return 1

        colecciones = {nombre: db[nombre] for nombre in COLECCIONES_AFECTADAS}
        con_datos = [
            nombre
            for nombre, coleccion in colecciones.items()
            if coleccion.count_documents({}, limit=1) > 0
        ]
        if con_datos:
            print(
                "Migración cancelada para proteger los datos. "
                "Estas colecciones no están vacías: "
                + ", ".join(con_datos)
            )
            return 1

        indices_normales = {
            nombre: {
                indice["name"]
                for indice in coleccion.list_indexes()
            }
            for nombre, coleccion in colecciones.items()
        }
        indices_vectoriales = {
            nombre: {
                indice["name"]
                for indice in coleccion.list_search_indexes()
            }
            for nombre, coleccion in colecciones.items()
        }
    except PyMongoError as error:
        print(
            "No se pudo comprobar que la migración sea segura "
            f"({type(error).__name__}); no se retiraron índices."
        )
        return 1
    except Exception as error:
        print(
            f"No se pudo preparar la migración ({type(error).__name__}). "
            "Revisa la conexión y la configuración."
        )
        return 1

    try:
        for nombre, indices in INDICES_NORMALES_OBSOLETOS.items():
            for indice in indices:
                if indice in indices_normales[nombre]:
                    colecciones[nombre].drop_index(indice)
                    print(f"Índice normal anterior retirado: {nombre}.{indice}")

        for nombre, indice in INDICES_VECTORIALES_OBSOLETOS.items():
            if indice in indices_vectoriales[nombre]:
                colecciones[nombre].drop_search_index(indice)
                print(f"Índice vectorial anterior retirado: {nombre}.{indice}")
    except PyMongoError as error:
        print(
            f"La migración de índices se detuvo ({type(error).__name__}). "
            "Revisa el estado actual en Atlas antes de volver a ejecutarla."
        )
        return 1

    from scripts.init_db import main as inicializar_db

    return inicializar_db()


if __name__ == "__main__":
    sys.exit(main())
