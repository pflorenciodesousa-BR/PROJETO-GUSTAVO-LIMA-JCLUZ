from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "telas"
OUT.mkdir(exist_ok=True)

W, H = 1080, 1350
M = 84

NAVY = "#071426"
NAVY_2 = "#0C1D35"
BLUE = "#2F6BFF"
COBALT = "#1147D7"
ICE = "#EAF0FF"
WARM = "#F4F0E7"
WHITE = "#FAFAF7"
GOLD = "#C8A45A"
INK = "#101D31"
MUTED = "#596579"

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def canvas(color):
    return Image.new("RGB", (W, H), color)


def add_grain(im, opacity=12, seed=7):
    random.seed(seed)
    noise = Image.effect_noise((W, H), 28).convert("L")
    noise = ImageEnhance.Contrast(noise).enhance(0.7)
    layer = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    layer.putalpha(noise.point(lambda p: int(p * opacity / 255)))
    return Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")


def base_art():
    source = Image.open(ROOT / "arte-base.png").convert("RGB")
    scale = max(W / source.width, H / source.height)
    size = (round(source.width * scale), round(source.height * scale))
    source = source.resize(size, Image.Resampling.LANCZOS)
    left = (source.width - W) // 2
    top = (source.height - H) // 2
    return source.crop((left, top, left + W, top + H))


def top_meta(draw, number, dark=True, label="CULTURA • JC LUZ"):
    color = ICE if dark else MUTED
    draw.text((M, 54), label, font=font(19, True), fill=color)
    num = f"{number:02d} / 08"
    bbox = draw.textbbox((0, 0), num, font=font(18, True))
    draw.text((W - M - (bbox[2] - bbox[0]), 54), num, font=font(18, True), fill=color)


def footer(draw, dark=True, hint=None):
    color = (234, 240, 255, 150) if dark else (16, 29, 49, 130)
    draw.line((M, H - 74, W - M, H - 74), fill=color, width=1)
    draw.rounded_rectangle((M, H - 50, M + 18, H - 32), radius=4, fill=BLUE)
    draw.text((M + 30, H - 55), "JC LUZ", font=font(17, True), fill=color)
    if hint:
        bbox = draw.textbbox((0, 0), hint, font=font(16, True))
        draw.text((W - M - (bbox[2] - bbox[0]), H - 54), hint, font=font(16, True), fill=color)


def line(draw, xy, text, size, color, bold=False, anchor=None, spacing=8):
    draw.multiline_text(xy, text, font=font(size, bold), fill=color, spacing=spacing, anchor=anchor)


def pill(draw, x, y, text, fill, color, width=None):
    f = font(19, True)
    bb = draw.textbbox((0, 0), text, font=f)
    tw = bb[2] - bb[0]
    pw = width or tw + 42
    draw.rounded_rectangle((x, y, x + pw, y + 48), radius=24, fill=fill)
    draw.text((x + 21, y + 11), text, font=f, fill=color)


def circle_crop(source, diameter, x, y, border=0, border_color=BLUE):
    crop = source.resize((diameter, diameter), Image.Resampling.LANCZOS)
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter, diameter), fill=255)
    holder = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    holder.paste(crop.convert("RGBA"), (x, y), mask)
    if border:
        ImageDraw.Draw(holder).ellipse((x, y, x + diameter, y + diameter), outline=border_color, width=border)
    return holder


def save(im, number):
    final = add_grain(im, opacity=8, seed=number)
    final.save(OUT / f"{number:02d}.png", quality=95)


ART = base_art()


# 01 — Capa
im = ART.copy().convert("RGBA")
shade = Image.new("RGBA", (W, H), (3, 12, 24, 0))
sd = ImageDraw.Draw(shade)
sd.rectangle((0, 0, W, H), fill=(3, 12, 24, 38))
sd.rectangle((0, 650, W, H), fill=(3, 12, 24, 128))
im = Image.alpha_composite(im, shade)
d = ImageDraw.Draw(im)
top_meta(d, 1, dark=True, label="JC LUZ • AGOSTO 2026")
pill(d, M, 715, "DESLIZE PARA OLHAR DE PERTO", (47, 107, 255, 235), WHITE)
line(d, (M, 790), "Toda empresa tem.", 72, WHITE, True)
line(d, (M, 886), "Poucas param\npara olhar.", 96, WHITE, True, spacing=2)
footer(d, dark=True, hint="→")
save(im, 1)


# 02 — Revelação
im = canvas(WARM).convert("RGBA")
d = ImageDraw.Draw(im)
top_meta(d, 2, dark=False)
im = Image.alpha_composite(im, circle_crop(ART, 520, 610, 135, border=3, border_color=BLUE))
d = ImageDraw.Draw(im)
line(d, (M, 260), "Estamos falando\nde", 58, INK, True, spacing=0)
line(d, (M, 388), "cultura.", 126, BLUE, True)
line(d, (M, 760), "Não a que fica escrita\nna parede.", 48, INK, True, spacing=6)
line(d, (M, 915), "A que aparece nas escolhas, nas conversas\ne no jeito como as pessoas trabalham\nquando o dia aperta.", 34, MUTED, False, spacing=12)
footer(d, dark=False)
save(im, 2)


# 03 — Definição
im = canvas(COBALT).convert("RGBA")
d = ImageDraw.Draw(im)
for x, y, r, alpha in [(720, 180, 430, 34), (820, 500, 560, 24), (780, 890, 460, 20)]:
    d.ellipse((x, y, x + r, y + r), outline=(244, 240, 231, alpha), width=4)
top_meta(d, 3, dark=True)
pill(d, M, 250, "O QUE É UM EVENTO DE CULTURA?", (244, 240, 231, 240), COBALT)
line(d, (M, 360), "Uma pausa\ncom propósito.", 98, WHITE, True, spacing=0)
line(d, (M, 650), "Um espaço para sair do automático\ne conversar sobre:", 32, ICE, False, spacing=8)
line(d, (M, 765), "quem somos,", 56, WHITE, True)
line(d, (M, 840), "o que queremos preservar", 56, WHITE, True)
line(d, (M, 915), "e o que precisa evoluir.", 56, WHITE, True)
footer(d, dark=True)
save(im, 3)


# 04 — Importância
im = canvas(NAVY).convert("RGBA")
d = ImageDraw.Draw(im)
top_meta(d, 4, dark=True)
d.ellipse((650, 135, 1220, 705), outline=(47, 107, 255, 150), width=5)
d.ellipse((770, 255, 1095, 580), fill=(47, 107, 255, 22), outline=(244, 240, 231, 70), width=2)
pill(d, M, 250, "POR QUE ISSO IMPORTA?", (47, 107, 255, 235), WHITE)
line(d, (M, 375), "A cultura não\ndeixa de existir", 78, WHITE, True, spacing=2)
line(d, (M, 585), "quando ninguém\nolha para ela.", 78, ICE, True, spacing=2)
line(d, (M, 860), "Ela apenas passa a ser construída", 35, ICE, False)
line(d, (M, 920), "pelo acaso.", 94, GOLD, True)
footer(d, dark=True)
save(im, 4)


# 05 — Participação
im = canvas(WHITE).convert("RGBA")
d = ImageDraw.Draw(im)
top_meta(d, 5, dark=False)
pill(d, M, 228, "QUANDO O TIME PARTICIPA", BLUE, WHITE)
line(d, (M, 350), "a cultura deixa\nde ser apenas", 74, INK, True, spacing=2)
line(d, (M, 548), "um conceito.", 104, BLUE, True)
d.line((M, 685, W - M, 685), fill="#CAD4E6", width=2)
line(d, (M, 760), "Ela ganha exemplos,\nconversas e atitudes", 58, INK, True, spacing=4)
line(d, (M, 940), "que todo mundo consegue reconhecer\nno dia a dia.", 36, MUTED, False, spacing=12)
d.ellipse((760, 930, 1040, 1210), outline=(47, 107, 255, 60), width=3)
d.ellipse((840, 1010, 1000, 1170), fill=(47, 107, 255, 22))
footer(d, dark=False)
save(im, 5)


# 06 — Virada JC Luz
blur = ART.filter(ImageFilter.GaussianBlur(2)).convert("RGBA")
overlay = Image.new("RGBA", (W, H), (4, 15, 31, 92))
im = Image.alpha_composite(blur, overlay)
d = ImageDraw.Draw(im)
top_meta(d, 6, dark=True, label="AQUI, A CONVERSA SE TORNA NOSSA")
pill(d, M, 280, "PELA PRIMEIRA VEZ", (200, 164, 90, 235), NAVY)
line(d, (M, 405), "Foi com esse olhar", 60, ICE, False)
line(d, (M, 500), "que a JC Luz", 104, WHITE, True)
line(d, (M, 635), "decidiu fazer\nalgo diferente.", 88, WHITE, True, spacing=0)
line(d, (M, 930), "Parar. Ouvir. Refletir. Construir juntos.", 34, ICE, False)
footer(d, dark=True)
save(im, 6)


# 07 — Evento
im = canvas(WARM).convert("RGBA")
d = ImageDraw.Draw(im)
top_meta(d, 7, dark=False)
line(d, (M, 235), "2", 208, BLUE, True)
line(d, (310, 284), "primeiras", 48, INK, True)
line(d, (310, 344), "semanas", 72, INK, True)
line(d, (310, 428), "de agosto", 42, MUTED, False)
d.line((M, 515, W - M, 515), fill="#BFCADD", width=2)
line(d, (M, 590), "Nosso primeiro\nevento de cultura.", 76, INK, True, spacing=2)
line(d, (M, 825), "Um tempo para ouvir, refletir e aproximar\nas pessoas da empresa que estamos\nconstruindo juntos.", 38, MUTED, False, spacing=14)
pill(d, M, 1070, "PRIMEIRO EVENTO • AGOSTO", NAVY, WHITE)
footer(d, dark=False)
save(im, 7)


# 08 — Fechamento
im = ART.copy().convert("RGBA")
overlay = Image.new("RGBA", (W, H), (3, 12, 24, 116))
im = Image.alpha_composite(im, overlay)
d = ImageDraw.Draw(im)
top_meta(d, 8, dark=True, label="CULTURA EM MOVIMENTO")
line(d, (M, 300), "O evento\nterminou.", 86, ICE, True, spacing=0)
line(d, (M, 545), "O olhar\nficou.", 118, WHITE, True, spacing=0)
d.line((M, 855, 420, 855), fill=GOLD, width=5)
line(d, (M, 905), "Cultura não acontece em uma data.\nEla aparece todos os dias — e é\nconstruída por todos nós.", 38, ICE, False, spacing=14)
footer(d, dark=True, hint="JC LUZ • 2026")
save(im, 8)


# Contact sheet para revisão rápida
thumb_w, thumb_h = 324, 405
sheet = Image.new("RGB", (thumb_w * 4 + 60, thumb_h * 2 + 40), "#DCE2EA")
for index in range(1, 9):
    slide = Image.open(OUT / f"{index:02d}.png").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    col = (index - 1) % 4
    row = (index - 1) // 4
    sheet.paste(slide, (12 + col * (thumb_w + 12), 12 + row * (thumb_h + 12)))
sheet.save(ROOT / "preview-carrossel.png", quality=95)

print(f"Carrossel exportado em: {OUT}")
