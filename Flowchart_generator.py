from pathlib import Path
from graphviz import Digraph


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

DIAGRAM_NAME = "diagramaFlujo"
OUTPUT_DIR = Path("output")

# Orientación: "TB" = arriba hacia abajo, "LR" = izquierda a derecha
ORIENTATION = "LR"

# Apariencia
FONT_NAME = "Arial"
FONT_SIZE = "22"
LINE_WIDTH = "2.2"

# Espaciado entre elementos
NODE_SEPARATION = "0.8"
RANK_SEPARATION = "0.4"


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
etapa1 = "Definición Formal del\n Espacio de Búsqueda y\n Representación (GP)."
etapa2 = "Definición de las \nFunciones Matemáticas \nPrimarias y Primitivas."
etapa3 = "Diseño de la Función\n de Aptitud (Fitness\n Function)."
etapa4 = "Operadores Genéticos\n y Estrategia de \nEvolución."
etapa5 = "Ensamblado y \nPipeline de \nGeneración Visual."
etapa6 = "Validación y \nAnálisis de \nResultados."

ELEMENTOS = [
    {
        "id": "e1",
        "tipo": "proceso",
        "texto": etapa1,
    },
    {
        "id": "e2",
        "tipo": "proceso",
        "texto": etapa2,
    },
    {
        "id": "e3",
        "tipo": "proceso",
        "texto": etapa3,
    },
    {
        "id": "e4",
        "tipo": "proceso",
        "texto": etapa4,
    },
    {
        "id": "e5",
        "tipo": "proceso",
        "texto": etapa5,
    },
   {
        "id": "e6",
        "tipo": "proceso",
        "texto": etapa6,
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
        "origen": "e1",
        "destino": "e2",
        "salida": "e",
        "entrada": "w",
    },
    {
        "origen": "e2",
        "destino": "e3",
        "salida": "e",
        "entrada": "w",
    },
    {
        "origen": "e3",
        "destino": "e4",
        "salida": "e",
        "entrada": "w",
    },
    {
        "origen": "e4",
        "destino": "e5",
        "salida": "e",
        "entrada": "w",
    },
    {
        "origen": "e5",
        "destino": "e6",
        "salida": "e",
        "entrada": "w",
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
    """Build the diagram using ELEMENTS and CONNECTIONS."""

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
        splines="ortho",
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
        fontsize="5",
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
                f"Duplicate identifier: {identificador}"
            )

        if tipo not in FORMAS:
            raise ValueError(
                f"Unrecognized element type: {tipo}"
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
    # Agregar las conexiones
    for conexion in CONEXIONES:

        origen = conexion["origen"]
        destino = conexion["destino"]
        etiqueta = conexion.get("etiqueta", "")

        if origen not in ids or destino not in ids:
            raise ValueError(
                f"Conexión inválida: {origen} -> {destino}"
            )

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
    """Export the diagram to the selected format."""

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

    print("\nDiagram generated successfully.")
    print(f"Formato: {extension.upper()}")
    print(f"Archivo: {Path(ruta).resolve()}")


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def main():
    print("=" * 45)
    print(" FLOWCHART GENERATOR")
    print("=" * 45)

    try:
        diagrama = generar_diagrama()
    except (ValueError, KeyError) as error:
        print(f"\nError while building the diagram: {error}")
        return

    print("\nSelect the export format:")
    print("1. JPG")
    print("2. PNG")
    print("3. SVG")
    print("4. All formats")

    opcion = input("\nOption: ").strip()

    if opcion == "4":
        for formato in ("1", "2", "3"):
            exportar_diagrama(diagrama, formato)
    else:
        exportar_diagrama(diagrama, opcion)


if __name__ == "__main__":
    main()