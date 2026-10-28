from pathlib import Path

import numpy as np
import imageio.v2 as imageio

from PIL import Image, ImageOps


# ============================================================
# CONFIGURACIÓN
# ============================================================

INPUT_DIR = Path("anmtn_images")
OUTPUT_DIR = Path("animation_output")

OUTPUT_GIF = OUTPUT_DIR / "animacion.gif"
OUTPUT_MP4 = OUTPUT_DIR / "animacion.mp4"

# Duración que permanece visible cada imagen, en segundos.
IMAGE_DURATION = 2.0

# Duración de la transición entre imágenes, en segundos.
TRANSITION_DURATION = 0.8

# Fotogramas por segundo del MP4.
FPS = 30

# Resolución de salida: (ancho, alto).
# None utiliza la resolución de la primera imagen.
OUTPUT_SIZE = (1280, 720)

# Tipos de transición:
# "fade"      -> fundido entre imágenes.
# "slide"     -> desplazamiento horizontal.
# "dissolve"  -> disolución progresiva.
TRANSITION = "fade"

# Calidad del MP4: valores entre 0 y 10.
# Un valor menor generalmente produce mejor calidad.
MP4_QUALITY = 6

# Repetir el GIF indefinidamente.
GIF_LOOP = 0

# Color de fondo para imágenes con transparencia.
BACKGROUND_COLOR = (255, 255, 255)


# ============================================================
# CARGA Y PREPARACIÓN DE IMÁGENES
# ============================================================

def load_images():
    """Carga las imágenes y las adapta a la resolución de salida."""

    if not INPUT_DIR.exists():
        raise FileNotFoundError(
            f"No existe la carpeta: {INPUT_DIR.resolve()}"
        )

    extensions = {
        ".png", ".jpg", ".jpeg", ".bmp", ".webp"
    }

    files = sorted(
        [
            path
            for path in INPUT_DIR.iterdir()
            if path.is_file()
            and path.suffix.lower() in extensions
        ],
        key=lambda path: path.name.lower()
    )

    if len(files) < 2:
        raise ValueError(
            "Se necesitan al menos dos imágenes en la carpeta images/."
        )

    images = []

    for file in files:
        with Image.open(file) as source:
            image = ImageOps.exif_transpose(source).convert("RGBA")

            if OUTPUT_SIZE is not None:
                image = ImageOps.contain(
                    image,
                    OUTPUT_SIZE,
                    method=Image.Resampling.LANCZOS
                )

                # Centrar la imagen sin deformarla.
                canvas = Image.new(
                    "RGBA",
                    OUTPUT_SIZE,
                    BACKGROUND_COLOR + (255,)
                )

                x = (OUTPUT_SIZE[0] - image.width) // 2
                y = (OUTPUT_SIZE[1] - image.height) // 2

                canvas.alpha_composite(image, (x, y))
                image = canvas

            else:
                image = image.convert("RGB")

            # Componer sobre el fondo para eliminar transparencia.
            background = Image.new(
                "RGBA",
                image.size,
                BACKGROUND_COLOR + (255,)
            )
            background.alpha_composite(image)

            images.append(
                background.convert("RGB")
            )

            print(f"Imagen cargada: {file.name}")

    return images


# ============================================================
# TRANSICIONES
# ============================================================

def interpolate_images(img1, img2, alpha):
    """Fundido progresivo entre dos imágenes."""

    return Image.blend(img1, img2, alpha)


def slide_transition(img1, img2, alpha):
    """La segunda imagen entra desde la derecha."""

    width, height = img1.size

    offset = int(width * alpha)

    frame = Image.new("RGB", (width, height))

    frame.paste(img1.crop((offset, 0, width, height)), (0, 0))

    frame.paste(
        img2.crop((0, 0, offset, height)),
        (width - offset, 0)
    )

    return frame


def dissolve_transition(img1, img2, alpha, seed):
    """Disolución espacial reproducible mediante una máscara aleatoria."""

    a = np.asarray(img1).astype(np.float32)
    b = np.asarray(img2).astype(np.float32)

    rng = np.random.default_rng(seed)

    # Una máscara fija evita que el ruido parpadee entre fotogramas.
    mask = rng.random(a.shape[:2])

    threshold = alpha

    # Suavizar ligeramente el borde de la disolución.
    softness = 0.04

    weight = np.clip(
        (threshold - mask + softness) / (2 * softness),
        0,
        1
    )

    weight = weight[:, :, None]

    result = a * (1 - weight) + b * weight

    return Image.fromarray(
        np.clip(result, 0, 255).astype(np.uint8)
    )


def make_transition(img1, img2, alpha, seed):
    """Selecciona la transición configurada."""

    if TRANSITION == "fade":
        return interpolate_images(img1, img2, alpha)

    if TRANSITION == "slide":
        return slide_transition(img1, img2, alpha)

    if TRANSITION == "dissolve":
        return dissolve_transition(img1, img2, alpha, seed)

    raise ValueError(
        f"Transición desconocida: {TRANSITION}"
    )


# ============================================================
# GENERACIÓN DE FOTOGRAMAS
# ============================================================

def generate_frames(images):
    """
    Genera la secuencia completa.

    Cada imagen permanece IMAGE_DURATION segundos.
    Entre imágenes se inserta una transición de
    TRANSITION_DURATION segundos.
    """

    hold_frames = max(1, round(IMAGE_DURATION * FPS))
    transition_frames = round(TRANSITION_DURATION * FPS)

    if IMAGE_DURATION <= 0:
        raise ValueError("IMAGE_DURATION debe ser mayor que cero.")

    if TRANSITION_DURATION < 0:
        raise ValueError("TRANSITION_DURATION no puede ser negativa.")

    if FPS <= 0:
        raise ValueError("FPS debe ser mayor que cero.")

    frames = []

    for i, image in enumerate(images):
        # Mantener la imagen visible durante el tiempo indicado.
        for _ in range(hold_frames):
            frames.append(image.copy())

        # Transición hacia la siguiente imagen.
        if i < len(images) - 1 and transition_frames > 0:
            next_image = images[i + 1]

            for step in range(1, transition_frames + 1):
                alpha = step / transition_frames

                frame = make_transition(
                    image,
                    next_image,
                    alpha,
                    seed=i
                )

                frames.append(frame)

    return frames


# ============================================================
# EXPORTACIÓN GIF
# ============================================================

def export_gif(frames):
    """Exporta los fotogramas a un GIF animado."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # GIF utiliza una paleta de hasta 256 colores por fotograma.
    gif_frames = [
        frame.convert("RGB").quantize(colors=256)
        for frame in frames
    ]

    gif_frames[0].save(
        OUTPUT_GIF,
        save_all=True,
        append_images=gif_frames[1:],
        duration=round(1000 / FPS),
        loop=GIF_LOOP,
        optimize=False,
        disposal=2
    )

    print(f"GIF generado: {OUTPUT_GIF.resolve()}")


# ============================================================
# EXPORTACIÓN MP4
# ============================================================

def export_mp4(frames):
    """Exporta los fotogramas a un vídeo MP4."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with imageio.get_writer(
        OUTPUT_MP4,
        format="FFMPEG",
        mode="I",
        fps=FPS,
        codec="libx264",
        quality=MP4_QUALITY,
        pixelformat="yuv420p",
        macro_block_size=16
    ) as writer:

        for i, frame in enumerate(frames):
            writer.append_data(
                np.asarray(frame.convert("RGB"))
            )

            if (i + 1) % FPS == 0:
                print(
                    f"Procesados {i + 1}/{len(frames)} fotogramas"
                )

    print(f"MP4 generado: {OUTPUT_MP4.resolve()}")


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():
    images = load_images()

    print(f"\nTotal de imágenes: {len(images)}")
    print(f"Resolución: {images[0].size}")
    print(f"FPS: {FPS}")
    print(f"Duración por imagen: {IMAGE_DURATION} s")
    print(f"Duración de transición: {TRANSITION_DURATION} s")
    print(f"Tipo de transición: {TRANSITION}")

    frames = generate_frames(images)

    duration = len(frames) / FPS

    print(f"\nTotal de fotogramas: {len(frames)}")
    print(f"Duración aproximada: {duration:.2f} s")

    export_gif(frames)
    export_mp4(frames)

    print("\nProceso terminado.")


if __name__ == "__main__":
    main()