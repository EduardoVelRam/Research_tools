from pathlib import Path
from graphviz import Digraph


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

DIAGRAM_NAME = "diagrama_flujo"
OUTPUT_DIR = Path("output")

# Orientación: "TB" = arriba hacia abajo, "LR" = izquierda a derecha
ORIENTATION = "TB"

# Apariencia
FONT_NAME = "Arial"
FONT_SIZE = "12"
LINE_WIDTH = "1.2"

# Espaciado entre elementos
NODE_SEPARATION = "0.5"
RANK_SEPARATION = "0.7"


# ============================================================
# DEFINICIÓN DE LOS ELEMENTOS
# ============================================================
#
# Tipos disponibles:
#
#   inicio    -> Óvalo
#   proceso   -> Rectángulo
#   decision  -> Rombo
#   entrada   -> Paralelogramo
#   fin       -> Óvalo
#
# Cada elemento tiene:
#   id     : identificador único
#   tipo   : tipo de figura
#   texto  : texto que aparece dentro de la figura
#
# ============================================================

ELEMENTOS = [
    {
        "id": "inicio",
        "tipo": "inicio",
        "texto": "Inicio",
    },
    {
        "id": "entrada",
        "tipo": "entrada",
        "texto": "Ingresar número",
    },
    {
        "id": "decision",
        "tipo": "decision",
        "texto": "¿El número es par?",
    },
    {
        "id": "par",
        "tipo": "proceso",
        "texto": "Mostrar 'Es par'",
    },
    {
        "id": "impar",
        "tipo": "proceso",
        "texto": "Mostrar 'Es impar'",
    },
    {
        "id": "fin",
        "tipo": "fin",
        "texto": "Fin",
    },
]


# ============================================================
# DEFINICIÓN DE LAS CONEXIONES
# ============================================================
#
# Cada conexión tiene:
#   origen  : id del elemento inicial
#   destino : id del elemento final
#   etiqueta: texto opcional junto a la flecha
#
# ============================================================

CONEXIONES = [
    {
        "origen": "inicio",
        "destino": "entrada",
        "salida": "s",
        "entrada": "n",
    },
    {
        "origen": "entrada",
        "destino": "decision",
        "salida": "s",
        "entrada": "n",
    },
    {
        "origen": "decision",
        "destino": "par",
        "etiqueta": "Sí",
        "salida": "w",
        "entrada": "e",
    },
    {
        "origen": "decision",
        "destino": "impar",
        "etiqueta": "No",
        "salida": "e",
        "entrada": "w",
    },
    {
        "origen": "par",
        "destino": "fin",
        "salida": "s",
        "entrada": "w",
    },
    {
        "origen": "impar",
        "destino": "entrada",
        "salida": "s",
        "entrada": "e",
    },
]


# ============================================================
# FORMAS DE LOS ELEMENTOS
# ============================================================

FORMAS = {
    "inicio": "ellipse",
    "proceso": "box",
    "decision": "diamond",
    "entrada": "parallelogram",
    "fin": "ellipse",
}


# ============================================================
# GENERACIÓN DEL DIAGRAMA
# ============================================================

def generar_diagrama():
    """Construye el diagrama a partir de ELEMENTOS y CONEXIONES."""

    diagrama = Digraph(
        name=DIAGRAM_NAME,
        format="png",
    )

    # Configuración general del diagrama
    diagrama.attr(
        rankdir=ORIENTATION,
        bgcolor="white",
        pad="0.25",
        nodesep=NODE_SEPARATION,
        ranksep=RANK_SEPARATION,
        splines="line",
        outputorder="edgesfirst",
    )

    # Configuración general de las figuras
    diagrama.attr(
        "node",
        style="filled",
        fillcolor="white",
        color="black",
        fontcolor="black",
        fontname=FONT_NAME,
        fontsize=FONT_SIZE,
        penwidth=LINE_WIDTH,
        margin="0.15,0.10",
    )

    # Configuración general de las flechas
    diagrama.attr(
        "edge",
        color="black",
        fontcolor="black",
        fontname=FONT_NAME,
        fontsize="10",
        penwidth=LINE_WIDTH,
        arrowsize="0.8",
    )

    # Registrar los identificadores existentes
    ids = set()

    # Agregar las figuras
    for elemento in ELEMENTOS:
        identificador = elemento["id"]
        tipo = elemento["tipo"]
        texto = elemento["texto"]

        if identificador in ids:
            raise ValueError(
                f"Identificador duplicado: {identificador}"
            )

        if tipo not in FORMAS:
            raise ValueError(
                f"Tipo de elemento no reconocido: {tipo}"
            )

        ids.add(identificador)

        diagrama.node(
            identificador,
            label=texto,
            shape=FORMAS[tipo],
        )

    # Agregar las conexiones
    # Agregar las conexiones
    # Agregar las conexiones
    for conexion in CONEXIONES:

        origen = conexion["origen"]
        destino = conexion["destino"]
        etiqueta = conexion.get("etiqueta", "")

        if origen not in ids or destino not in ids:
            raise ValueError(
                f"Conexión inválida: {origen} -> {destino}"
            )

        # Puntos centrales de las figuras
        puerto_salida = conexion.get("salida", "s")
        puerto_entrada = conexion.get("entrada", "n")

        diagrama.edge(
            f"{origen}:{puerto_salida}",
            f"{destino}:{puerto_entrada}",
            label=etiqueta,
        )

    return diagrama


# ============================================================
# EXPORTACIÓN
# ============================================================

def exportar_diagrama(diagrama, formato):
    """Exporta el diagrama al formato seleccionado."""

    formatos_validos = {
        "1": "jpg",
        "2": "png",
        "3": "svg",
    }

    if formato not in formatos_validos:
        print("Formato no válido.")
        return

    extension = formatos_validos[formato]

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Configurar el formato de salida
    diagrama.format = extension

    # Exportar el archivo
    ruta = diagrama.render(
        filename=DIAGRAM_NAME,
        directory=str(OUTPUT_DIR),
        cleanup=True,
    )

    print("\nDiagrama generado correctamente.")
    print(f"Formato: {extension.upper()}")
    print(f"Archivo: {Path(ruta).resolve()}")


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def main():
    print("=" * 45)
    print(" GENERADOR DE DIAGRAMAS DE FLUJO")
    print("=" * 45)

    try:
        diagrama = generar_diagrama()
    except (ValueError, KeyError) as error:
        print(f"\nError al construir el diagrama: {error}")
        return

    print("\nSelecciona el formato de exportación:")
    print("1. JPG")
    print("2. PNG")
    print("3. SVG")
    print("4. Todos los formatos")

    opcion = input("\nOpción: ").strip()

    if opcion == "4":
        for formato in ("1", "2", "3"):
            exportar_diagrama(diagrama, formato)
    else:
        exportar_diagrama(diagrama, opcion)


if __name__ == "__main__":
    main()