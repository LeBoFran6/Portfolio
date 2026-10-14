"""Build the real-asset portfolio: optimise images out of the Wix export into the
site tree. Idempotent. Run from anywhere."""
import os, sys, io, json, shutil, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

SRC = r"C:\Users\Fran6\Documents\GitHub\_wix_source_backup\assets\img"
DST = r"C:\Users\Fran6\Documents\GitHub\Portfolio\assets\img"
REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"
FF  = subprocess.run([sys.executable, "-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"],
                     capture_output=True, text=True).stdout.strip()

def src(n):
    return os.path.join(SRC, n)

def out(rel):
    """rel is a site-root-relative path (e.g. assets/img/projects/x.webp)."""
    p = os.path.join(REPO, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p

def webp(rel, name, maxw=1600, q=82, crop=None):
    """Convert a source image to webp at the site. Returns (relpath, w, h)."""
    im = Image.open(src(name)); im.seek(0); im = im.convert("RGB")
    if crop:                                   # (aspect_w, aspect_h, gravity)
        aw, ah, g = crop
        target = aw / ah
        w, h = im.size
        if w / h > target:                     # too wide -> crop sides
            nw = int(h * target); x = (w - nw) // 2 if g == "c" else 0
            im = im.crop((x, 0, x + nw, h))
        else:                                  # too tall -> crop top/bottom
            nh = int(w / target)
            y = int((h - nh) * 0.38) if g == "t" else (h - nh) // 2
            im = im.crop((0, y, w, y + nh))
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = out(rel)
    im.save(p, "WEBP", quality=q, method=6)
    return rel, im.width, im.height

def gifframe(rel, name, frame=0, maxw=1280, q=84):
    im = Image.open(src(name)); im.seek(frame); im = im.convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    p = out(rel)
    im.save(p, "WEBP", quality=q, method=6)
    return rel, im.width, im.height

# ----------------------------------------------------------------- manifest
# ph_id -> {"hero": (srcfile, alt, caption), "gallery": [(srcfile, alt, caption), ...]}
W  = "4d02d36d-2ec010_51d4e456c3124669a3a25027d0376a7c_mv2.jpg"

M = {
"warno": dict(
  hero=("4d02d36d-2ec010_51d4e456c3124669a3a25027d0376a7c_mv2.jpg",
        "In-engine editor view of a production map, with a region selected and the navigation overlays live",
        "The production map in the studio's in-house engine editor."),
  gallery=[
   ("7302660b-2ec010_16475012110244c7805e440e6d25a5b8_mv2.jpg",
    "Real-time in-game view of an armoured column moving through a wheat field under smoke",
    "Real-time target look, in engine."),
   ("f69fc4b3-2ec010_0d6cdd4361ff4f78bf0fef77545bb71a_mv2.png",
    "Aerial view of a lake and forest crossing, built to real-world scale",
    "Terrain and water at map scale."),
   ("e0080ff5-2ec010_f5000f6133264727855da8f929ff2b29_mv2.png",
    "Top-down view of farmland, hedgerows and a road network across the map",
    "The road network that makes the map read like satellite imagery."),
   ("d6020c94-2ec010_7025279a9c654dcdb6c2f199932958ff_mv2.png",
    "A small town built from modular kits, seen from above",
    "One modular kit, varied across instances."),
   ("9f8502b8-2ec010_7025279a9c654dcdb6c2f199932958ff_mv2.png",
    "A riverside settlement with a bridge and a treeline",
    "Scale and proportion held across a whole district."),
   ("4d92540b-2ec010_d8cc80abd40a4f489085832531d797a7_mv2.png",
    "A residential diorama: detached house, road markings, parked cars and garden",
    "A populated block diorama, randomised per placement."),
   ("739940ac-2ec010_8521b2979ceb4ad08d125f7b52e4843c_mv2.png",
    "A disused airfield diorama: runway, taxiway and scattered ground clutter",
    "Landmark props, built from the same kit language."),
   ("3213427b-2ec010_c40270d9f1fa46ca8308a28233219b91_mv2.png",
    "An industrial site with pipework and storage tanks on a grass field",
    "Industrial variant of the environment kit."),
  ]),

"rubber": dict(
  hero=("3ab913df-2ec010_80f904b3703a4e569a6c1dc9e47974e7_mv2.png",
        "RUBBER key art: the retro-futuristic taxi against a neon city skyline",
        "RUBBER â€” the vehicle that is the main character of the game."),
  gallery=[
   ("80cd4d3f-2ec010_37e71410a069494caccb0f7ebb1f0299_mv2.png",
    "Driving at night down a neon street, HUD showing score and multiplier",
    "In-game driving at night."),
   ("2518770a-2ec010_7b387f633a414ee2bee3ce1b139e8786_mv2.jpg",
    "The retro-futuristic city: dense signage, wet asphalt and coloured lighting",
    "The city the car was tuned against."),
   ("66557c36-2ec010_e7387e1bb182411a801ff614f8f3be75_mv2.jpg",
    "The taxi front-on in a garage bay, showing the custom body and lighting",
    "Front-on: the vehicle's stance and surfacing."),
   ("89337f19-2ec010_474da467f08544c6a4246b70796c4e59_mv2.png",
    "Top-down layout of the building kit in 3ds Max, props laid out by category",
    "Kit assembly in 3ds Max before export."),
   ("70a1ddf9-2ec010_f466ac2c8702426ea3eb658dd9b6f0f3_mv2.png",
    "The taxi in the 3ds Max viewport with the modifier stack open",
    "Modelling in 3ds Max â€” Nanite means one high-definition model only."),
   ("7f55fea6-2ec010_0c423d1b520d45de96bdbe5f128c7281_mv2.png",
    "The vehicle in wireframe with Morpher targets highlighted for detachment",
    "Morpher targets: each panel detaches independently on impact."),
   ("02e900d2-2ec010_0c423d1b520d45de96bdbe5f128c7281_mv2.png",
    "The same vehicle in vertex colours, showing the mask separation used for destruction",
    "Vertex-colour masks drive the detachment."),
   ("6e6d8fe1-2ec010_ad38658a25cf4c7bb05b2e6ff8f8942f_mv2.jpg",
    "The car producing smoke as it slides, showing the feedback layer in motion",
    "Drift feedback: smoke, audio and camera shake together."),
   ("6825731c-2ec010_32fe2648c66e4d16b90c381c7ffe3320_mv2.jpg",
    "The car mid-drift with debris lifting off the road surface",
    "Landing and drift feedback."),
  ]),

"fittingbox": dict(
  hero=("a062b013-2ec010_953d22f4f30e4e09a83909b32ff423cd_mv2.jpg",
        "Eyewear product visualisation for a virtual try-on: frames, lenses and a model studio background",
        "Virtual try-on delivered for international eyewear brands."),
  gallery=[
   ("96347d33-2ec010_df2d2b433ae44d0e942bd42896a4c4d3_mv2.jpg",
    "Face tracking running on a webcam feed, with the landmark mesh overlaid on the subject",
    "Runtime face tracking â€” the frames have to sit on a moving face."),
   ("efad48e6-2ec010_c2a68435d2e246a1ac203d979180daa5_mv2.jpg",
    "Virtual try-on interface with a live rating and product panel",
    "The try-on UI in the browser."),
   ("604b245d-2ec010_1d1e0c3a34c0441a83b8ed986d0cba02_mv2.png",
    "Metal aviator frame rendered on a clean studio background",
    "Asset fidelity target: studio-grade product renders, web budgets."),
   ("aeb65bf2-2ec010_6a21b6f1fc1549d486a02a0331a6a35a_mv2.png",
    "Tortoiseshell acetate frame rendered on a clean studio background",
    "Same budget, harder material: layered acetate."),
   ("967898a6-2ec010_5bbc2f8f001646668835e1af703ce1f5_mv2.png",
    "Black cat-eye frame rendered on a clean studio background",
    "Gloss and transparency held under a bandwidth budget."),
   ("90a859b5-2ec010_5bbc2f8f001646668835e1af703ce1f5_mv2.png",
    "Round metal frame rendered on a clean studio background",
    "Thin metal geometry, anti-aliased without extra draw calls."),
   ("13d83c6e-2ec010_b2649c6970824e3c8dc76d454a17b4f9_mv2.png",
    "Red sports wraparound frame rendered on a clean studio background",
    "Tinted lens, reflective coating."),
   ("f5684e1a-2ec010_0230667c7e044285b0b9ca7d58b2a200_mv2.png",
    "Thin rectangular metal frame rendered on a clean studio background",
    "Hundreds of these per month, all under the same budget."),
   ("905dc160-2ec010_c56e2e4ed43a48578406f0cc4d10b3f6_mv2.png",
    "Architectural glass and steel structure shot from below",
    "Material studies carried over from arch-viz work."),
  ]),

"automated-blender-render-pipeline": dict(
  hero=("1b810e40-2ec010_2328286bf9d64706adac65a0c3a94189_mv2.gif",
        "A Windows file explorer window open on the render drop folder, with the one-click batch file selected",
        "The whole workflow: artists drop a delivery into this folder and double-click."),
  gallery=[
   ("aa05388d-Capture_PNG.png",
    "Blender open with a geometry node graph and a Python console running the batch script",
    "The headless Python pass: validate, assemble, resolve, render."),
   ("1422f0b5-dd_PNG.png",
    "Blender viewport showing four rigged game characters assembled in one scene",
    "4 characters, one automatically assembled scene."),
   ("8f9aabc1-dd_PNG.png",
    "Blender viewport with the assembled character scene and the render panel open",
    "Scene assembly is deterministic â€” the same input gives the same output."),
   ("26ad7fbd-Capture_PNG.png",
    "Blender with the node graph and output configuration visible in a second capture",
    "Materials and animation data resolved without an engineer in the loop."),
  ]),

"lets-sing-voxler": dict(
  hero=("140f98aa-2ec010_37fc3c5c11dd402591d66fcfe4a2c87f_mv2.jpg",
        "An animated karaoke character mid-performance with a microphone, lit against a stage gradient",
        "Character render pass â€” one of the four shipped every year."),
  gallery=[
   ("9f406f60-2ec010_9843ae2886234688bd712a603810f119_mv2.jpg",
    "Full-body karaoke character on a lit stage, mid-performance",
    "Authored animation, rendered frame by frame by the pipeline."),
   ("0a951b6a-2ec010_9843ae2886234688bd712a603810f119_mv2.jpg",
    "Wide stage view with the character, lighting rig and crowd elements",
    "Stage lighting and VFX held to a fixed art direction."),
   ("78a7d843-2ec010_c2a68435d2e246a1ac203d979180daa5_mv2.jpg",
    "Close-up of a rendered face mid-performance",
    "The runtime gaze system: eyes track events independently of the baked animation."),
   ("efad48e6-2ec010_c2a68435d2e246a1ac203d979180daa5_mv2.jpg",
    "A close facial capture used to check gaze tracking against the authored performance",
    "Gaze validated against authored performance."),
   ("b9c03e00-2ec010_01bff0df1a68462383014839f102b32c_mv2.jpg",
    "Performance frame with the stage wash and rim lighting",
    "Glow, bloom and VFX R&D under a fixed frame budget."),
  ]),

"environment-art": dict(
  hero=("f8b12fa3-2ec010_0e0a05c891754a2fa9b2e539808c14bc_mv2.png",
        "A real-time desert landscape with sand dunes, scrub and a cactus under a clouded sky",
        "Environment art â€” the domain where my artistic inclination is strongest."),
  gallery=[
   ("8bf5b416-2ec010_60ee85a94b2e42dd9a58191c01026d6a_mv2.png",
    "Desert landscape from a second angle, showing the dune shape and horizon",
    "The same scene from a second camera."),
   ("fdfb45ad-2ec010_0e0a05c891754a2fa9b2e539808c14bc_mv2.png",
    "Close desert view showing scrub, cactus and sand detail at ground level",
    "Ground-level detail holds up when the player gets close."),
   ("fa7de245-2ec010_bab61ab82bf14eb9a34f49a13a721610_mv2.png",
    "Wind-carved sand ridges in close detail",
    "Terrain detail, sculpted in World Machine."),
   ("5d23cc62-2ec010_66d58c8d9a444b70b9ff3b44bfa0132b_mv2.png",
    "Three World Machine device graphs side by side: erosion, macro shape and detail passes",
    "World Machine node graphs â€” built by iteration, then imported into the engine."),
   ("508c3c00-2ec010_7f1a6f0a98b945a8ac976b019fb9f31b_mv2.png",
    "Aerial view across a large settlement and its surrounding farmland",
    "Large-scale layout and terrain, read at map scale."),
   ("e0080ff5-2ec010_f5000f6133264727855da8f929ff2b29_mv2.png",
    "Top-down view of terrain with roads and field boundaries",
    "Procedural terrain laid out for a playable space."),
  ]),

"architectural-visualisation": dict(
  hero=("76f16571-2ec010_e1b66e8ea1b24d0097b2b9d9fdb3b3eb_mv2.png",
        "Real-time architectural visualisation of a timber-clad house with a garden and stepped terraces",
        "Architectural visualisation â€” real-time, not an offline render."),
  gallery=[
   ("7678341c-2ec010_e1b66e8ea1b24d0097b2b9d9fdb3b3eb_mv2.png",
    "The same house from the opposite elevation, showing the terraces and garden slope",
    "Second elevation."),
   ("da8bb5f6-2ec010_3fcc9fd4236649a99a2318659e103673_mv2.png",
    "The house from a raised three-quarter angle, showing the roof form and deck",
    "Roof form and deck."),
   ("13452c2f-2ec010_e1b66e8ea1b24d0097b2b9d9fdb3b3eb_mv2.png",
    "Street-level view of the house and its immediate surroundings",
    "In context, at eye height."),
   ("5355efd4-2ec010_3fcc9fd4236649a99a2318659e103673_mv2.png",
    "The house seen across the neighbouring garden and hedge line",
    "Neighbouring plots â€” consistency across a set."),
   ("47b35bbb-2ec010_cca4e77cdc8b4413b7ac36bdef1c68cc_mv2.png",
    "The house with planting and boundary treatment in place",
    "Landscaping pass."),
   ("0b0965cd-2ec010_60ee85a94b2e42dd9a58191c01026d6a_mv2.png",
    "The house against the sky, showing the cladding material response",
    "Cladding material under a real-time sky."),
  ]),

"dietemna": dict(
  hero=("313db9c2-2ec010_1a07491e42194c6a8dc6d8966816c125_mv2.png",
        "An isometric cutaway of a submarine hold lit by a single swinging lamp",
        "DIETEMNA â€” a horror game about a submarine that should not have gone down."),
  gallery=[
   ("cab85ae7-2ec010_3ae4b5e2e3514d528696fa3db683a2d9_mv2.png",
    "A flooded section of the submarine lit green, with the water line visible",
    "The flooding set."),
   ("fc7f870f-2ec010_bf2a62e7308847ab885eed64b0909bf9_mv2.png",
    "The engine room of the submarine, lit by a single warm lamp",
    "Engine room."),
   ("06a73869-2ec010_d728c036a78e414cb03ae08503b548e4_mv2.png",
    "A debris-filled corridor of the submarine with the HUD timer running",
    "One of the three rooms, in play."),
   ("33938d28-2ec010_fbf7d26d44b448758d6d7bbcb0247c75_mv2.png",
    "The hold with crates and barrels scattered by the swell",
    "Set dressing and lighting pass."),
   ("156b7436-1.png",
    "A narrow submarine corridor with photographs pinned along the wall",
    "The corridor set, photographed in engine."),
   ("e74a1644-7.png",
    "The submarine cockpit with instruments lit in blue and green",
    "Cockpit."),
   ("602ef1ab-2.png",
    "Machinery space with pipework and a single overhead light",
    "Machinery space."),
  ]),

"game-jams": dict(
  hero=("7d2703a6-2ec010_182cdf2b70ed4b6686379cef2ca48845_mv2.png",
        "A cel-shaded kart racer in a flooded industrial arena, viewed from behind the player's kart",
        "Game jams â€” what gets built in 48 to 72 hours."),
  gallery=[
   ("0c5db8e4-2ec010_3700a56d83404bfea47bef581b0ccafe_mv2.png",
    "The same arena from a second run, with the rival kart ahead",
    "Same build, different run."),
   ("9761d2e3-2ec010_f7c0530a9e1449e3906c1f596aafe3e7_mv2.png",
    "A match-four puzzle game with tree-growth cards on a purple board",
    "Global Game Jam 2023 â€” theme: Roots."),
   ("de8f3c45-2ec010_03d8801c8ab148c78d6ed838f8617524_mv2.png",
    "A first-person arena shooter with a phase counter and a win state shown",
    "First-person arena prototype."),
   ("5cfa3aed-2ec010_9ef5546008ff49c9ab71f95fc2b707c0_mv2.png",
    "The same shooter with destructible objects highlighted as damage volumes",
    "Destructible props â€” the system carried into RUBBER."),
  ]),
}

# ------------------------------------------------------------------ render
report = {}
for slug, spec in M.items():
    rows = {}
    h = spec["hero"]
    rows["hero"] = webp(f"assets/img/projects/{slug}-hero.webp", h[0], maxw=1600, q=82)
    gal = []
    for i, (f, alt, cap) in enumerate(spec["gallery"], 1):
        rel, w, hh = webp(f"assets/img/projects/{slug}-g{i:02d}.webp", f, maxw=1100, q=80)
        gal.append(dict(rel=rel, w=w, h=hh, alt=alt, cap=cap))
    rows["gallery"] = gal
    rows["hero_alt"] = h[1]
    rows["hero_cap"] = h[2]
    report[slug] = rows
    print(f"{slug:36s} hero {rows['hero'][1]}x{rows['hero'][2]}  +{len(gal)} gallery")

# portrait
report["portrait"] = webp("assets/img/about/portrait.webp",
    "b2410112-2ec010_47239f2863f84d52b971dd7f056aef02_mv2.jpg", maxw=900, q=86)
print("portrait", report["portrait"][1], "x", report["portrait"][2])

json.dump(report, open(r"C:\Users\Fran6\Documents\GitHub\Portfolio\_assets.json", "w"), indent=1)
print("\nTOTAL webp:", round(sum(os.path.getsize(os.path.join(dp, f))
      for dp, _, fs in os.walk(DST) for f in fs) / 1048576, 2), "MB")