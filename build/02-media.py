import os, sys, io, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None

BK = r"C:\Users\Fran6\Documents\GitHub\_wix_source_backup"
REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"
FF = subprocess.run([sys.executable, "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
                    capture_output=True, text=True).stdout.strip()

# ---------------------------------------------------------------- 1. video
os.makedirs(os.path.join(REPO, "assets", "media"), exist_ok=True)
srcv = os.path.join(BK, "assets", "media", "22c43710-file.mp4")
dstv = os.path.join(REPO, "assets", "media", "environment-clip.mp4")
subprocess.run([FF, "-y", "-i", srcv,
                "-vf", "scale=1600:-2,fps=30",
                "-c:v", "libx264", "-profile:v", "high", "-crf", "23",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "-an", dstv], check=True, capture_output=True)
print("video", round(os.path.getsize(dstv) / 1048576, 2), "MB")

# poster frame from the clip (a moment with the tyre + guitar framed well)
post = os.path.join(REPO, "assets", "img", "reel", "environment-clip-poster.webp")
os.makedirs(os.path.dirname(post), exist_ok=True)
subprocess.run([FF, "-y", "-ss", "00:00:03", "-i", dstv, "-frames:v", "1",
                "-q:v", "3", os.path.join(BK, "_poster.png")], check=True, capture_output=True)
im = Image.open(os.path.join(BK, "_poster.png")).convert("RGB")
im.save(post, "WEBP", quality=84, method=6)
print("poster", im.size)

# ------------------------------------------------------------ 2. OG card
OGW, OGH = 1200, 630
try:
    F_DISP = ImageFont.truetype("impact.ttf", 92)
    F_MONO = ImageFont.truetype("cour.ttf", 26)
    F_MONO2 = ImageFont.truetype("cour.ttf", 22)
except Exception:
    F_DISP = F_MONO = F_MONO2 = ImageFont.load_default()

base = Image.open(os.path.join(BK, "assets", "img", "80cd4d3f-2ec010_37e71410a069494caccb0f7ebb1f0299_mv2.png")).convert("RGB")
bw, bh = base.size
scale = max(OGW / bw, OGH / bh)
base = base.resize((round(bw * scale), round(bh * scale)), Image.LANCZOS)
x = (base.width - OGW) // 2
y = (base.height - OGH) // 2
card = base.crop((x, y, x + OGW, y + OGH))

# darken with a left-weighted gradient so the type stays legible
grad = Image.new("L", (OGW, OGH), 0)
gd = ImageDraw.Draw(grad)
for i in range(OGW):
    gd.line([(i, 0), (i, OGH)], fill=int(255 * max(0.0, 1 - i / 1000)))
dark = Image.new("RGB", (OGW, OGH), (10, 10, 10))
card = Image.composite(dark, card, grad)
card = Image.blend(card, Image.new("RGB", (OGW, OGH), (12, 11, 11)), 0.42)

d = ImageDraw.Draw(card)
YEL = (255, 222, 52)
WHT = (255, 248, 246)
MUT = (200, 190, 188)
# accent bar
d.rectangle([56, 60, 56 + 10, 60 + 78], fill=YEL)
d.text((92, 56), "FRANCISCO DE CARVALHO PEREIRA", font=F_MONO, fill=YEL)
d.text((56, 150), "TECHNICAL ARTIST", font=F_DISP, fill=WHT)
d.text((56, 232), "/ TECHNICAL DIRECTOR", font=F_DISP, fill=WHT)
d.text((56, 336), "Real-time 3D  \u00b7  pipeline automation  \u00b7  console optimisation",
       font=F_MONO2, fill=MUT)
d.text((56, 372), "Unreal Engine 5  \u00b7  Unity  \u00b7  Blender / Python  \u00b7  C#",
       font=F_MONO2, fill=MUT)
d.rectangle([56, 430, 56 + 300, 430 + 4], fill=(153, 149, 148))
d.text((56, 452), "6 CONSOLE TARGETS   \u00b7   300+ ASSETS / MONTH", font=F_MONO2, fill=WHT)
d.text((56, 484), "SHIPPED WORK  \u00b7  BREAKDOWNS  \u00b7  CV", font=F_MONO2, fill=MUT)

ogp = os.path.join(REPO, "assets", "img", "og", "og-cover-1200x630.jpg")
os.makedirs(os.path.dirname(ogp), exist_ok=True)
card.save(ogp, "JPEG", quality=86, optimize=True, progressive=True)
print("og", card.size, round(os.path.getsize(ogp) / 1024), "KB")

# ----------------------------------------------------------------- 3. CV
cv_src = os.path.join(BK, "assets", "files",
                      "62b24489-2ec010_f436b036a95d44a8831cfd9c3978b48b.pdf")
cv_dst = os.path.join(REPO, "assets", "files", "cv-francisco-de-carvalho-pereira.pdf")
os.makedirs(os.path.dirname(cv_dst), exist_ok=True)
shutil.copy2(cv_src, cv_dst)
print("cv", round(os.path.getsize(cv_dst) / 1024), "KB")