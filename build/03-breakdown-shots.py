import os, sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from PIL import Image

REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"
BK   = r"C:\Users\Fran6\Documents\GitHub\_wix_source_backup"
SRC  = os.path.join(BK, "assets", "img")
DST  = os.path.join(REPO, "assets", "img", "breakdown")
os.makedirs(DST, exist_ok=True)
Image.MAX_IMAGE_PIXELS = None

# PH-RD id -> (source file, out name, alt)
RD = {
 "PH-RD-02": ("aa05388d-Capture_PNG.png", "material-regeneration-node-graph.webp",
   "Blender open with a geometry node graph and a Python console running the batch script"),
 "PH-RD-03": ("1b810e40-2ec010_2328286bf9d64706adac65a0c3a94189_mv2.gif", "headless-blender-pipeline.webp",
   "A Windows file explorer window open on the render drop folder with the one-click batch file selected", 24),
 "PH-RD-04": ("1422f0b5-dd_PNG.png", "unity-animation-validation-tool.webp",
   "Blender viewport showing four rigged game characters assembled in one scene"),
 "PH-RD-05": ("7f55fea6-2ec010_0c423d1b520d45de96bdbe5f128c7281_mv2.png", "chaos-vehicle-rig.webp",
   "The vehicle in wireframe with its custom six-wheel rig and suspension nodes visible"),
 "PH-RD-06": ("02e900d2-2ec010_0c423d1b520d45de96bdbe5f128c7281_mv2.png", "morpher-destruction.webp",
   "The vehicle in vertex colours showing the mask separation that drives panel detachment"),
 "PH-RD-07": ("5d23cc62-2ec010_66d58c8d9a444b70b9ff3b44bfa0132b_mv2.png", "world-machine-node-graph.webp",
   "Three World Machine device graphs side by side: erosion, macro shape and detail passes"),
 "PH-RD-08": ("4d02d36d-2ec010_51d4e456c3124669a3a25027d0376a7c_mv2.jpg", "draw-call-profiler.webp",
   "In-engine editor view of a production map with region selection and navigation overlays"),
 "PH-RD-10": ("78a7d843-2ec010_c2a68435d2e246a1ac203d979180daa5_mv2.jpg", "runtime-gaze-system.webp",
   "Close-up of a rendered face mid-performance, showing decoupled eye and pupil control"),
 "PH-RD-11": ("f69fc4b3-2ec010_0d6cdd4361ff4f78bf0fef77545bb71a_mv2.png", "world-streaming-sectors.webp",
   "Aerial view of a lake and forest crossing in a large-scale streamed world"),
 "PH-RD-12": ("76f16571-2ec010_e1b66e8ea1b24d0097b2b9d9fdb3b3eb_mv2.png", "cad-repair-before-after.webp",
   "Real-time architectural visualisation of a timber-clad house with garden and terraces"),
 "PH-RD-01": ("80cd4d3f-2ec010_37e71410a069494caccb0f7ebb1f0299_mv2.png", "scene-capture-frame-time.webp",
   "In-game frame with the performance HUD live, showing score, multiplier and frame instrumentation"),
}

meta = {}
for pid, rec in RD.items():
    fname, outname, alt = rec[0], rec[1], rec[2]
    frame = rec[3] if len(rec) > 3 else 0
    im = Image.open(os.path.join(SRC, fname)); im.seek(frame); im = im.convert("RGB")
    if im.width > 1100:
        im = im.resize((1100, round(im.height * 1100 / im.width)), Image.LANCZOS)
    p = os.path.join(DST, outname)
    im.save(p, "WEBP", quality=82, method=6)
    meta[pid] = dict(rel=f"assets/img/breakdown/{outname}", w=im.width, h=im.height, alt=alt)
    print(f"{pid}  {im.width}x{im.height}  {outname}")

json.dump(meta, open(os.path.join(BK, "_breakdown.json"), "w"), indent=1)
print("\nbreakdown assets:", round(sum(os.path.getsize(os.path.join(DST, f))
      for f in os.listdir(DST)) / 1024), "KB")