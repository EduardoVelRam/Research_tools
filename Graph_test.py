
import numpy as np
import matplotlib.pyplot as plt

# 1. GENERAL CONFIGURATION

RANDOM_SEED = 42
N = 50

# Tipo de visualización:
# "line", "scatter", "both", "bar"
PLOT_TYPE = "both"

# Elementos opcionales
SHOW_GRID = True
SHOW_LEGEND = True
SHOW_MEAN = True
SHOW_STD = True
SHOW_ERROR_BARS = False
SHOW_ZERO_LINE = False

# Configuración de ejes
SHOW_X_LIMITS = False
SHOW_Y_LIMITS = False

X_LIMITS = (0, 50)
Y_LIMITS = (-3, 3)

# Etiquetas
TITLE = "Comparación de tres conjuntos de datos sintéticos"
X_LABEL = "Observación"
Y_LABEL = "Valor"

# Exportación
SAVE_FIGURE = True
OUTPUT_NAME = "synthetic_plot"
OUTPUT_FORMAT = "png"  # png, jpg, svg
DPI = 300


# 2. SYNTETIC DATA GENERATION

np.random.seed(RANDOM_SEED)

x = np.arange(N)

# Conjunto 1: señal sinusoidal con ruido
data_1 = np.sin(x * 0.15) + np.random.normal(0, 0.20, N)

# Conjunto 2: tendencia lineal con ruido
data_2 = np.linspace(-1, 1, N) + np.random.normal(0, 0.25, N)

# Conjunto 3: señal periódica diferente
data_3 = np.cos(x * 0.12) + np.random.normal(0, 0.20, N)

datasets = {
    "Conjunto 1": data_1,
    "Conjunto 2": data_2,
    "Conjunto 3": data_3
}


# 3. FIGURE AND AXIS CREATION

fig, ax = plt.subplots(figsize=(12, 6))

# Estilos individuales
styles = {
    "Conjunto 1": {
        "color": "tab:blue",
        "marker": "o",
        "linestyle": "-"
    },
    "Conjunto 2": {
        "color": "tab:orange",
        "marker": "s",
        "linestyle": "--"
    },
    "Conjunto 3": {
        "color": "tab:green",
        "marker": "^",
        "linestyle": "-."
    }
}


# 4. DATA PLOTTING

for name, data in datasets.items():

    style = styles[name]

    if PLOT_TYPE == "line":
        ax.plot(
            x, data,
            label=name,
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=1.8
        )

    elif PLOT_TYPE == "scatter":
        ax.scatter(
            x, data,
            label=name,
            color=style["color"],
            marker=style["marker"],
            s=35
        )

    elif PLOT_TYPE == "both":
        ax.plot(
            x, data,
            color=style["color"],
            linestyle=style["linestyle"],
            linewidth=1.5,
            alpha=0.8
        )

        ax.scatter(
            x, data,
            label=name,
            color=style["color"],
            marker=style["marker"],
            s=25
        )

    elif PLOT_TYPE == "bar":
        width = 0.25
        offset = list(datasets.keys()).index(name) * width

        ax.bar(
            x + offset,
            data,
            width=width,
            label=name,
            color=style["color"],
            alpha=0.75
        )


# 5. STATISTICAL ELEMENTS

for name, data in datasets.items():

    style = styles[name]

    mean = np.mean(data)
    std = np.std(data)

    if SHOW_MEAN:
        ax.axhline(
            mean,
            color=style["color"],
            linestyle=":",
            linewidth=1.5,
            alpha=0.8
        )

    if SHOW_STD:
        ax.axhspan(
            mean - std,
            mean + std,
            color=style["color"],
            alpha=0.08
        )

    if SHOW_ERROR_BARS:
        ax.errorbar(
            x,
            data,
            yerr=std * 0.1,
            fmt="none",
            ecolor=style["color"],
            alpha=0.3,
            capsize=2
        )


# 6. REFERENCE ELEMENTS

if SHOW_ZERO_LINE:
    ax.axhline(
        0,
        color="black",
        linestyle="--",
        linewidth=1,
        alpha=0.7
    )

if SHOW_GRID:
    ax.grid(
        True,
        linestyle="--",
        linewidth=0.6,
        alpha=0.5
    )


# 7. AXIS AND LABELS CONFIGURATION

ax.set_title(TITLE, fontsize=15, fontweight="bold")
ax.set_xlabel(X_LABEL, fontsize=12)
ax.set_ylabel(Y_LABEL, fontsize=12)

if SHOW_X_LIMITS:
    ax.set_xlim(X_LIMITS)

if SHOW_Y_LIMITS:
    ax.set_ylim(Y_LIMITS)

if SHOW_LEGEND:
    ax.legend(fontsize=10, loc="best")

ax.tick_params(axis="both", labelsize=10)

plt.tight_layout()


# 8. VISUALIZATION AND EXPORT

if SAVE_FIGURE:
    plt.savefig(
        f"{OUTPUT_NAME}.{OUTPUT_FORMAT}",
        dpi=DPI,
        bbox_inches="tight"
    )

plt.show()
