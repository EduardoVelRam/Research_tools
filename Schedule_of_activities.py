import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class CronogramaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Cronogramas")
        self.root.geometry("1100x650")

        # Datos iniciales
        self.periodos = [
            "P1", "P2", "P3", "P4",
            "P5", "P6", "P7", "P8"
        ]

        self.actividades = [
            "Revisión bibliográfica",
            "Diseño de la metodología",
            "Implementación",
            "Experimentación",
            "Análisis de resultados"
        ]

        # Matriz:
        # matriz[fila][columna] = True/False
        self.matriz = [
            [True, True, False, False, False, False, False, False],
            [False, True, True, True, False, False, False, False],
            [False, False, True, True, True, True, False, False],
            [False, False, False, False, True, True, True, False],
            [False, False, False, False, False, True, True, True],
        ]

        self.crear_interfaz()
        self.actualizar_tabla()

    # ---------------------------------------------------------
    # INTERFAZ
    # ---------------------------------------------------------

    def crear_interfaz(self):

        # Barra superior
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill="x", padx=10, pady=10)

        ttk.Button(
            toolbar,
            text="Agregar actividad",
            command=self.agregar_actividad
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Eliminar actividad",
            command=self.eliminar_actividad
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Subir actividad",
            command=self.subir_actividad
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Bajar actividad",
            command=self.bajar_actividad
        ).pack(side="left", padx=3)

        ttk.Separator(
            toolbar,
            orient="vertical"
        ).pack(side="left", fill="y", padx=8)

        ttk.Button(
            toolbar,
            text="Agregar periodo",
            command=self.agregar_periodo
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Eliminar periodo",
            command=self.eliminar_periodo
        ).pack(side="left", padx=3)

        ttk.Separator(
            toolbar,
            orient="vertical"
        ).pack(side="left", fill="y", padx=8)

        ttk.Button(
            toolbar,
            text="Exportar SVG",
            command=lambda: self.exportar("svg")
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Exportar EPS",
            command=lambda: self.exportar("eps")
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Exportar PNG",
            command=lambda: self.exportar("png")
        ).pack(side="left", padx=3)

        # Área de tabla
        self.frame_tabla = ttk.Frame(self.root)
        self.frame_tabla.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # ---------------------------------------------------------
    # TABLA
    # ---------------------------------------------------------

    def actualizar_tabla(self):

        # Eliminar tabla anterior
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        # Scrollbars
        canvas = tk.Canvas(self.frame_tabla)

        scrollbar_y = ttk.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=canvas.yview
        )

        scrollbar_x = ttk.Scrollbar(
            self.frame_tabla,
            orient="horizontal",
            command=canvas.xview
        )

        canvas.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        tabla = ttk.Frame(canvas)

        canvas.create_window(
            (0, 0),
            window=tabla,
            anchor="nw"
        )

        # ---------------------------------------------
        # Encabezado
        # ---------------------------------------------

        ttk.Label(
            tabla,
            text="Actividad",
            anchor="center",
            relief="solid"
        ).grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=1,
            pady=1
        )

        for j, periodo in enumerate(self.periodos):

            entry = ttk.Entry(
                tabla,
                width=12,
                justify="center"
            )

            entry.insert(0, periodo)

            entry.grid(
                row=0,
                column=j + 1,
                sticky="nsew",
                padx=1,
                pady=1
            )

            # Actualizar nombre al perder foco
            entry.bind(
                "<FocusOut>",
                lambda event, index=j, widget=entry:
                self.cambiar_periodo(index, widget)
            )

        # ---------------------------------------------
        # Actividades
        # ---------------------------------------------

        for i, actividad in enumerate(self.actividades):

            entry = ttk.Entry(
                tabla,
                width=30
            )

            entry.insert(0, actividad)

            entry.grid(
                row=i + 1,
                column=0,
                sticky="nsew",
                padx=1,
                pady=1
            )

            entry.bind(
                "<FocusOut>",
                lambda event, index=i, widget=entry:
                self.cambiar_actividad(index, widget)
            )

            for j in range(len(self.periodos)):

                estado = self.matriz[i][j]

                boton = tk.Button(
                    tabla,
                    text="●" if estado else "",
                    width=8,
                    height=1,
                    relief="solid",
                    command=lambda r=i, c=j:
                    self.alternar_celda(r, c)
                )

                if estado:
                    boton.configure(
                        background="#4CAF50",
                        foreground="white"
                    )

                boton.grid(
                    row=i + 1,
                    column=j + 1,
                    sticky="nsew",
                    padx=1,
                    pady=1
                )

        # Actualizar región desplazable
        tabla.update_idletasks()

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    # ---------------------------------------------------------
    # EDICIÓN DE CELDAS
    # ---------------------------------------------------------

    def alternar_celda(self, fila, columna):

        self.matriz[fila][columna] = not self.matriz[fila][columna]

        self.actualizar_tabla()

    # ---------------------------------------------------------
    # ACTIVIDADES
    # ---------------------------------------------------------

    def agregar_actividad(self):

        nombre = f"Nueva actividad {len(self.actividades) + 1}"

        self.actividades.append(nombre)

        self.matriz.append(
            [False] * len(self.periodos)
        )

        self.actualizar_tabla()

    def eliminar_actividad(self):

        if len(self.actividades) <= 1:
            messagebox.showwarning(
                "Aviso",
                "Debe existir al menos una actividad."
            )
            return

        indice = len(self.actividades) - 1

        self.actividades.pop()
        self.matriz.pop()

        self.actualizar_tabla()

    def subir_actividad(self):

        if len(self.actividades) < 2:
            return

        indice = len(self.actividades) - 1

        if indice == 0:
            return

        self.actividades[indice], self.actividades[indice - 1] = (
            self.actividades[indice - 1],
            self.actividades[indice]
        )

        self.matriz[indice], self.matriz[indice - 1] = (
            self.matriz[indice - 1],
            self.matriz[indice]
        )

        self.actualizar_tabla()

    def bajar_actividad(self):

        if len(self.actividades) < 2:
            return

        indice = len(self.actividades) - 1

        if indice >= len(self.actividades) - 1:
            return

        self.actividades[indice], self.actividades[indice + 1] = (
            self.actividades[indice + 1],
            self.actividades[indice]
        )

        self.matriz[indice], self.matriz[indice + 1] = (
            self.matriz[indice + 1],
            self.matriz[indice]
        )

        self.actualizar_tabla()

    # ---------------------------------------------------------
    # PERIODOS
    # ---------------------------------------------------------

    def agregar_periodo(self):

        numero = len(self.periodos) + 1

        self.periodos.append(f"P{numero}")

        for fila in self.matriz:
            fila.append(False)

        self.actualizar_tabla()

    def eliminar_periodo(self):

        if len(self.periodos) <= 1:
            messagebox.showwarning(
                "Aviso",
                "Debe existir al menos un periodo."
            )
            return

        self.periodos.pop()

        for fila in self.matriz:
            fila.pop()

        self.actualizar_tabla()

    # ---------------------------------------------------------
    # CAMBIAR NOMBRES
    # ---------------------------------------------------------

    def cambiar_actividad(self, indice, widget):

        texto = widget.get().strip()

        if texto:
            self.actividades[indice] = texto

    def cambiar_periodo(self, indice, widget):

        texto = widget.get().strip()

        if texto:
            self.periodos[indice] = texto

    # ---------------------------------------------------------
    # GENERACIÓN DEL CRONOGRAMA
    # ---------------------------------------------------------

    def generar_figura(self):

        n_actividades = len(self.actividades)
        n_periodos = len(self.periodos)

        # Tamaño dinámico
        ancho = max(10, n_periodos * 1.1)
        alto = max(4, n_actividades * 0.7)

        fig, ax = plt.subplots(
            figsize=(ancho, alto)
        )

        # ---------------------------------------------
        # Dibujar actividades
        # ---------------------------------------------

        for i in range(n_actividades):

            y = n_actividades - i - 1

            for j in range(n_periodos):

                activo = self.matriz[i][j]

                if activo:

                    rect = Rectangle(
                        (j, y),
                        1,
                        0.8,
                        facecolor="steelblue",
                        edgecolor="black",
                        linewidth=0.8
                    )

                    ax.add_patch(rect)

                else:

                    rect = Rectangle(
                        (j, y),
                        1,
                        0.8,
                        facecolor="white",
                        edgecolor="lightgray",
                        linewidth=0.5
                    )

                    ax.add_patch(rect)

        # ---------------------------------------------
        # Ejes
        # ---------------------------------------------

        ax.set_xlim(0, n_periodos)
        ax.set_ylim(0, n_actividades)

        ax.set_xticks(
            [i + 0.5 for i in range(n_periodos)]
        )

        ax.set_xticklabels(
            self.periodos
        )

        ax.set_yticks(
            [i + 0.4 for i in range(n_actividades)]
        )

        ax.set_yticklabels(
            list(reversed(self.actividades))
        )

        ax.set_xlabel("Periodo")
        ax.set_ylabel("Actividad")

        ax.set_title(
            "Cronograma de actividades"
        )

        # Grid vertical
        ax.set_xticks(
            range(n_periodos + 1),
            minor=True
        )

        ax.grid(
            which="minor",
            axis="x",
            linewidth=0.5
        )

        plt.tight_layout()

        return fig

    # ---------------------------------------------------------
    # EXPORTACIÓN
    # ---------------------------------------------------------

    def exportar(self, formato):

        extensiones = {
            "svg": ".svg",
            "eps": ".eps",
            "png": ".png"
        }

        archivo = filedialog.asksaveasfilename(
            defaultextension=extensiones[formato],
            filetypes=[
                (
                    formato.upper(),
                    f"*{extensiones[formato]}"
                )
            ]
        )

        if not archivo:
            return

        try:

            fig = self.generar_figura()

            fig.savefig(
                archivo,
                format=formato,
                bbox_inches="tight"
            )

            plt.close(fig)

            messagebox.showinfo(
                "Exportación",
                f"Cronograma exportado correctamente:\n\n{archivo}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No fue posible exportar:\n\n{e}"
            )


# =============================================================
# PROGRAMA PRINCIPAL
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = CronogramaApp(root)

    root.mainloop()