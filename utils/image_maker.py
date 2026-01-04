from PIL import Image, ImageDraw, ImageFont
import os

BG_PATH = "media/bg.jpg"
FONT_PATH = "media/font.ttf"   # চাইলে default font use করো

def make_image(title, subtitle, avatar_path=None, out="media/out.jpg"):
    bg = Image.open(BG_PATH).convert("RGBA")
    draw = ImageDraw.Draw(bg)

    try:
        font_title = ImageFont.truetype(FONT_PATH, 48)
        font_sub = ImageFont.truetype(FONT_PATH, 32)
    except:
        font_title = font_sub = ImageFont.load_default()

    W, H = bg.size

    draw.text((W//2-200, 50), title, fill="white", font=font_title)
    draw.text((W//2-200, 120), subtitle, fill="white", font=font_sub)

    if avatar_path and os.path.exists(avatar_path):
        avatar = Image.open(avatar_path).resize((300, 300)).convert("RGBA")
        bg.paste(avatar, (W//2-150, H//2-150), avatar)

    bg.save(out)
    return out
