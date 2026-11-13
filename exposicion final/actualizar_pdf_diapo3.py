# -*- coding: utf-8 -*-
"""Solo diapo 3: barra amarilla + MH + chequeo predictivo. Copia nueva del PDF."""
from __future__ import annotations

from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
SRC = BASE / "compañeros" / "Incertidumbre en ventas de muebles y hogar.pdf"
OUT = BASE / "compañeros" / "Incertidumbre en ventas de muebles y hogar_actualizado.pdf"

# Escala nativa del PDF (cada página es imagen 3840×2160)
W, H = 3840, 2160
BG = (246, 245, 240)
NAVY = (18, 32, 47)
MUTED = (110, 119, 126)
BODY = (74, 85, 96)
YELLOW = (232, 178, 58)
WHITE = (255, 255, 255)
FONT = Path(r"C:\Windows\Fonts\segoeui.ttf")
FONT_B = Path(r"C:\Windows\Fonts\segoeuib.ttf")


def load_page_image(doc: pymupdf.Document, page_index: int) -> Image.Image:
    page = doc[page_index]
    xref = page.get_images()[0][0]
    pix = pymupdf.Pixmap(doc, xref)
    if pix.alpha:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    assert pix.width == W and pix.height == H, (pix.width, pix.height)
    return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)


def load_slide3() -> Image.Image:
    doc = pymupdf.open(SRC)
    img = load_page_image(doc, 2)
    doc.close()
    return img


def rounded_rect(draw, xy, radius, fill, outline=None):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)


def wrap(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# Tarjeta inferior derecha: recorte exacto del PNG original (mismo tamaño que las demás)
CARD_BR = (2406, 1434, 3583, 1787)


def patch_mcmc_card(img: Image.Image) -> None:
    """Restaura el recuadro original y solo reemplaza el texto interior."""
    orig = img.copy()
    x0, y0, x1, y1 = CARD_BR
    img.paste(orig.crop((x0, y0, x1, y1)), (x0, y0))

    draw = ImageDraw.Draw(img)
    # Interior de la tarjeta (sin tocar borde ni esquinas redondeadas)
    clear = (2488, 1502, 3538, 1746)
    draw.rectangle(clear, fill=WHITE)

    # Mismo margen izquierdo que «24 meses · probar» (≈175 px desde el borde de la tarjeta)
    tx, ty = 2583, 1516
    max_w = 3538 - tx - 8
    title_f = ImageFont.truetype(str(FONT_B), 56)
    body_f = ImageFont.truetype(str(FONT), 44)
    body_color = (68, 80, 94)

    draw.text((tx, ty), "Metropolis–Hastings", fill=NAVY, font=title_f)
    y = ty + 62
    draw.text((tx, y), "4 cadenas", fill=NAVY, font=title_f)
    y += 70
    body = (
        "R-hat < 1,01; 16 parámetros; priors débiles. "
        "Chequeo predictivo en entrenamiento."
    )
    for line in wrap(draw, body, body_f, max_w):
        draw.text((tx, y), line, fill=body_color, font=body_f)
        y += 52


def add_yellow_bar(img: Image.Image) -> None:
    """Misma banda amarilla que diapositiva 1 (posición por debajo del grid)."""
    draw = ImageDraw.Draw(img)
    bar = (260, 1825, 3579, 1974)
    rounded_rect(draw, bar, 48, YELLOW)
    font = ImageFont.truetype(str(FONT_B), 50)
    text = "Asociación contemporánea · no pronóstico con anticipación."
    draw.text((305, 1875), text, fill=NAVY, font=font)


def build_pdf(slide3: Image.Image) -> None:
    src = pymupdf.open(SRC)
    out = pymupdf.open()
    tmp = BASE / "compañeros" / "_slide3_patched.png"
    slide3.save(tmp, "PNG")

    for i in range(len(src)):
        page = out.new_page(width=960, height=540)
        rect = pymupdf.Rect(0, 0, 960, 540)
        if i == 2:
            page.insert_image(rect, filename=str(tmp))
        else:
            img = load_page_image(src, i)
            buf = BASE / "compañeros" / f"_page_{i}.png"
            img.save(buf, "PNG")
            page.insert_image(rect, filename=str(buf))
            buf.unlink(missing_ok=True)

    out.set_metadata({"title": "Incertidumbre en ventas de muebles y hogar (actualizado)"})
    out.save(OUT)
    out.close()
    src.close()
    tmp.unlink(missing_ok=True)


def main():
    img = load_slide3()
    patch_mcmc_card(img)
    add_yellow_bar(img)
    build_pdf(img)
    print("OK:", OUT)


if __name__ == "__main__":
    main()
