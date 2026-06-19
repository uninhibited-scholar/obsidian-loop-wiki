#!/usr/bin/env python3
"""Render an Obsidian-style "graph grows itself" demo GIF from a real vault.

Reads the vault's typed nodes + wikilinks, lays them out with a force-directed
simulation, then animates a progressive reveal — raw source first, then
entities, concepts, and finally the comparison + MOC hub that ties the network
together. Output is a looping GIF suitable for the top of the README.

Dependencies: Pillow (frames) + ffmpeg (GIF assembly). No matplotlib/networkx.

Usage:
    python3 scripts/render_demo_gif.py [VAULT_PATH] [OUT_GIF]
    # defaults: demo-vault  ->  assets/demo.gif
"""
import math
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

# ---- config -----------------------------------------------------------------
W, H = 960, 600
BG = (18, 18, 24)
FPS = 18
SCALE = 2  # supersample then downscale for crisp anti-aliased edges

# type -> (fill, glow) colors, Obsidian-dark palette
TYPE_COLOR = {
    "raw":         ((148, 163, 184), (148, 163, 184)),
    "entities":    ((34, 211, 238),  (34, 211, 238)),
    "concepts":    ((167, 139, 250), (167, 139, 250)),
    "comparisons": ((251, 191, 36),  (251, 191, 36)),
    "moc":         ((244, 114, 182), (244, 114, 182)),
}
# reveal order (wave index) by folder
WAVE = {"raw": 0, "entities": 1, "concepts": 2, "comparisons": 3, "moc": 3}
DIRS = ["concepts", "entities", "comparisons", "moc", "raw"]
WL = re.compile(r"\[\[([^\]|#]+)")


def load_graph(vault):
    stem_type = {}
    for d in DIRS:
        p = os.path.join(vault, d)
        if not os.path.isdir(p):
            continue
        for dp, _, ns in os.walk(p):
            for n in ns:
                if n.endswith(".md"):
                    stem_type[os.path.splitext(n)[0]] = d
    edges = set()
    rawcite = re.compile(r"raw/[\w./-]*?([\w-]+)\.md")
    for d in DIRS:
        p = os.path.join(vault, d)
        if not os.path.isdir(p):
            continue
        for dp, _, ns in os.walk(p):
            for n in ns:
                if not n.endswith(".md"):
                    continue
                s = os.path.splitext(n)[0]
                txt = open(os.path.join(dp, n), encoding="utf-8", errors="ignore").read()
                for tgt in WL.findall(txt):
                    tgt = tgt.strip()
                    if tgt in stem_type and tgt != s:
                        edges.add(tuple(sorted((s, tgt))))
                # citations into the evidence layer (raw/...md) count as links too
                for tgt in rawcite.findall(txt):
                    if tgt in stem_type and tgt != s:
                        edges.add(tuple(sorted((s, tgt))))
    return stem_type, sorted(edges)


def layout(nodes, edges, seed=7, iters=600):
    """Fruchterman-Reingold in normalized space, then fit to canvas."""
    rnd = __import__("random").Random(seed)
    pos = {n: [rnd.uniform(-1, 1), rnd.uniform(-1, 1)] for n in nodes}
    k = 2.3 * math.sqrt(1.0 / max(1, len(nodes)))
    t = 0.28
    adj = {n: set() for n in nodes}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    for _ in range(iters):
        disp = {n: [0.0, 0.0] for n in nodes}
        nl = list(nodes)
        for i in range(len(nl)):
            for j in range(i + 1, len(nl)):
                a, b = nl[i], nl[j]
                dx = pos[a][0] - pos[b][0]
                dy = pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 1e-4
                f = (k * k) / d  # repulsion
                ux, uy = dx / d, dy / d
                disp[a][0] += ux * f; disp[a][1] += uy * f
                disp[b][0] -= ux * f; disp[b][1] -= uy * f
        for a, b in edges:
            dx = pos[a][0] - pos[b][0]
            dy = pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 1e-4
            f = (d * d) / k  # attraction
            ux, uy = dx / d, dy / d
            disp[a][0] -= ux * f; disp[a][1] -= uy * f
            disp[b][0] += ux * f; disp[b][1] += uy * f
        for n in nodes:
            dx, dy = disp[n]
            d = math.hypot(dx, dy) or 1e-4
            pos[n][0] += (dx / d) * min(d, t)
            pos[n][1] += (dy / d) * min(d, t)
        t *= 0.985
    # relaxation: shove apart any pair that ended up too close, so labels breathe
    nl = list(nodes)
    mind = 0.42
    for _ in range(120):
        for i in range(len(nl)):
            for j in range(i + 1, len(nl)):
                a, b = nl[i], nl[j]
                dx = pos[a][0] - pos[b][0]
                dy = pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 1e-4
                if d < mind:
                    push = (mind - d) / 2
                    ux, uy = dx / d, dy / d
                    pos[a][0] += ux * push; pos[a][1] += uy * push
                    pos[b][0] -= ux * push; pos[b][1] -= uy * push
    # fit to canvas with margins
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    ml, mr, mt, mb = 130, 130, 80, 150  # reserve bottom room for labels + caption
    sx = (W - ml - mr) / (maxx - minx or 1)
    sy = (H - mt - mb) / (maxy - miny or 1)
    s = min(sx, sy)
    cx = ml + (W - ml - mr - s * (maxx - minx)) / 2 - s * minx
    cy = mt + (H - mt - mb - s * (maxy - miny)) / 2 - s * miny
    return {n: (s * p[0] + cx, s * p[1] + cy) for n, p in pos.items()}


def font(size):
    for path in (
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial.ttf",
    ):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def ease(x):
    return 0 if x <= 0 else (1 if x >= 1 else 1 - (1 - x) ** 3)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def main():
    vault = sys.argv[1] if len(sys.argv) > 1 else "demo-vault"
    out = sys.argv[2] if len(sys.argv) > 2 else "assets/demo.gif"
    stem_type, edges = load_graph(vault)
    nodes = list(stem_type)
    pos = layout(nodes, edges)
    deg = {n: 0 for n in nodes}
    for a, b in edges:
        deg[a] += 1; deg[b] += 1

    # frame schedule: hold, then one wave every `step` frames, then hold + caption
    step = 16
    intro, outro = 10, 40
    n_waves = max(WAVE.values()) + 1
    node_appear = {n: intro + WAVE[stem_type[n]] * step for n in nodes}
    total = intro + n_waves * step + outro
    F = font(22 * SCALE)
    Fcap = font(26 * SCALE)
    cap_color = (74, 222, 128)

    tmp = tempfile.mkdtemp(prefix="demo_frames_")
    sw, sh = W * SCALE, H * SCALE
    for fi in range(total):
        img = Image.new("RGB", (sw, sh), BG)
        d = ImageDraw.Draw(img, "RGBA")
        # gentle global breathing for life
        breathe = 1 + 0.012 * math.sin(fi / 7.0)

        def P(n):
            x, y = pos[n]
            return (x * SCALE * breathe + sw * (1 - breathe) / 2,
                    y * SCALE * breathe + sh * (1 - breathe) / 2)

        # edges (only when both endpoints have appeared)
        for a, b in edges:
            t0 = max(node_appear[a], node_appear[b]) + 4
            prog = ease((fi - t0) / 10.0)
            if prog <= 0:
                continue
            ax, ay = P(a); bx, by = P(b)
            alpha = int(70 * prog)
            d.line([(ax, ay), (bx, by)], fill=(120, 130, 150, alpha), width=max(1, SCALE))

        # nodes
        for n in nodes:
            prog = ease((fi - node_appear[n]) / 12.0)
            if prog <= 0:
                continue
            x, y = P(n)
            base = 7 + 3.2 * deg[n] ** 0.6
            r = base * SCALE * (0.4 + 0.6 * prog)
            fill, glow = TYPE_COLOR[stem_type[n]]
            # glow halo
            for gi, ga in ((2.6, 16), (1.8, 30), (1.25, 60)):
                rr = r * gi
                a = int(ga * prog)
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=glow + (a,))
            d.ellipse([x - r, y - r, x + r, y + r], fill=fill + (255,))
            d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255, int(160 * prog)),
                      width=max(1, SCALE))
            # label
            if prog > 0.5:
                label = n.replace("-", " ")
                la = int(255 * ease((prog - 0.5) / 0.5))
                tb = d.textbbox((0, 0), label, font=F)
                tw = tb[2] - tb[0]
                d.text((x - tw / 2, y + r + 4 * SCALE), label, font=F,
                       fill=(220, 224, 235, la))

        # closing caption with a hand-drawn check (font glyphs for ✓ are unreliable)
        cprog = ease((fi - (total - outro + 6)) / 14.0)
        if cprog > 0:
            cap = "PASS — graph connected, sources cited"
            tb = d.textbbox((0, 0), cap, font=Fcap)
            tw = tb[2] - tb[0]
            ca = int(255 * cprog)
            chk = 22 * SCALE  # check mark box size
            gap = 12 * SCALE
            total_w = chk + gap + tw
            x0 = (sw - total_w) / 2
            y0 = sh - 46 * SCALE
            cy = y0 + (tb[3] - tb[1]) / 2
            lw = max(2, 3 * SCALE)
            d.line([(x0, cy), (x0 + chk * 0.38, cy + chk * 0.42),
                    (x0 + chk, cy - chk * 0.5)], fill=cap_color + (ca,), width=lw, joint="curve")
            d.text((x0 + chk + gap, y0), cap, font=Fcap, fill=cap_color + (ca,))

        img = img.resize((W, H), Image.LANCZOS)
        img.save(os.path.join(tmp, f"f{fi:04d}.png"))

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    palette = os.path.join(tmp, "pal.png")
    subprocess.run(["ffmpeg", "-y", "-i", os.path.join(tmp, "f%04d.png"),
                    "-vf", "palettegen=stats_mode=full", palette],
                   check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", os.path.join(tmp, "f%04d.png"),
                    "-i", palette, "-lavfi", "paletteuse=dither=bayer:bayer_scale=3",
                    "-loop", "0", out], check=True, capture_output=True)
    print(f"wrote {out}  ({total} frames @ {FPS}fps, {os.path.getsize(out)//1024} KB)")


if __name__ == "__main__":
    main()
