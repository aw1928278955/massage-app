"""產生 App 圖示：深色底、金色進度環（呼應 75 小時門檻）加「75」。"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

root = pathlib.Path(__file__).resolve().parent.parent
BG, GOLD, TRACK = (13, 18, 23), (205, 174, 99), (42, 56, 67)
S = 2048  # 超取樣畫布

def font(size):
    for p in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
              "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

def base():
    im = Image.new("RGBA", (S, S), BG + (255,))
    d = ImageDraw.Draw(im)
    c, r, w = S // 2, int(S * 0.33), int(S * 0.085)
    box = (c - r, c - r, c + r, c + r)
    d.arc(box, 0, 360, fill=TRACK, width=w)
    d.arc(box, -90, 180, fill=GOLD, width=w)            # 270 度，像是快滿 75 小時
    for ang in (-90, 180):                                # 圓角端點
        import math
        rc = r - w / 2   # PIL 的弧線寬度往內畫，筆劃中心線半徑要減半個線寬
        x = c + rc * math.cos(math.radians(ang)); y = c + rc * math.sin(math.radians(ang))
        d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=GOLD)
    f = font(int(S * 0.25))
    t = "75"
    bb = d.textbbox((0, 0), t, font=f)
    d.text((c - (bb[0] + bb[2]) / 2, c - (bb[1] + bb[3]) / 2), t, font=f, fill=GOLD)
    return im

def rounded(im, frac=0.22):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.size[0] - 1, im.size[1] - 1), radius=int(im.size[0] * frac), fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out

def circle(im):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, im.size[0] - 1, im.size[1] - 1), fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0)); out.paste(im, (0, 0), m); return out

def save(im, path, size):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.resize((size, size), Image.LANCZOS).save(path)

art = base()
www = root / "www"
save(art.convert("RGB"), www / "icon-512.png", 512)
save(art.convert("RGB"), www / "icon-192.png", 192)
save(art.convert("RGB"), www / "apple-touch-icon.png", 180)
for folder, px in (("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)):
    d = root / "assets" / "android-res" / ("mipmap-" + folder)
    save(rounded(art), d / "ic_launcher.png", px)
    save(circle(art), d / "ic_launcher_round.png", px)
print("icons ok")
