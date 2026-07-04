#!/usr/bin/env python3
"""
Procedural placeholder art generator.

Produces quiet, abstract, duotone SVG compositions used as decorative
header art (journal posts, home hero, About portrait) — the real diary
entries themselves use actual photos in assets/covers/*.jpg, not this.
"""
import math
import random
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JOURNAL = [
    dict(slug="on-drawing-from-photos", bg="#F0EEE4", a="#7C8A6E", b="#D9C9A3", seed=11),
    dict(slug="eight-volumes-in", bg="#E9E7E4", a="#2B2B2E", b="#B0524B", seed=12),
    dict(slug="studio-notes-spring", bg="#EFEDE6", a="#6E8CA0", b="#C9D6C0", seed=13),
]

GRAIN_FILTER = """
    <filter id="grain-{sid}">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="{seed}" result="noise"/>
      <feColorMatrix in="noise" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.02 0"/>
      <feComposite operator="over" in2="SourceGraphic"/>
    </filter>
"""


def _rng(seed):
    return random.Random(seed)


def blob_path(cx, cy, r, rnd, points=8, wobble=0.22):
    pts = []
    for i in range(points):
        ang = (i / points) * math.pi * 2
        rr = r * (1 + rnd.uniform(-wobble, wobble))
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} "
    n = len(pts)
    for i in range(n):
        p0 = pts[i]
        p1 = pts[(i + 1) % n]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        d += f"Q {p0[0]:.1f} {p0[1]:.1f} {mx:.1f} {my:.1f} "
    d += "Z"
    return d


def composition(w, h, c, kind):
    rnd = _rng(c["seed"] * 97 + hash(kind) % 1000)
    sid = f"{c['slug']}-{kind}"
    cx, cy = w / 2, h / 2
    shapes = []

    shapes.append(f'<rect width="{w}" height="{h}" fill="{c["bg"]}"/>')

    g1 = rnd.uniform(0.55, 0.85)
    shapes.append(f'''<defs>
      <radialGradient id="g-{sid}" cx="{30+rnd.randint(0,40)}%" cy="{20+rnd.randint(0,30)}%" r="90%">
        <stop offset="0%" stop-color="{c['a']}" stop-opacity="{g1:.2f}"/>
        <stop offset="100%" stop-color="{c['bg']}" stop-opacity="0"/>
      </radialGradient>
      {GRAIN_FILTER.format(sid=sid, seed=c['seed'])}
    </defs>''')
    shapes.append(f'<rect width="{w}" height="{h}" fill="url(#g-{sid})"/>')

    big_r = min(w, h) * rnd.uniform(0.30, 0.42)
    bx = cx + rnd.uniform(-w * 0.12, w * 0.12)
    by = cy + rnd.uniform(-h * 0.12, h * 0.12)
    shapes.append(f'<path d="{blob_path(bx, by, big_r, rnd)}" fill="{c["b"]}" opacity="0.55"/>')

    small_r = big_r * rnd.uniform(0.35, 0.55)
    sx = bx + rnd.uniform(-big_r, big_r) * 0.6
    sy = by + rnd.uniform(-big_r, big_r) * 0.6
    shapes.append(f'<path d="{blob_path(sx, sy, small_r, rnd, points=6)}" fill="{c["a"]}" opacity="0.35"/>')

    for i in range(rnd.randint(2, 3)):
        r = min(w, h) * rnd.uniform(0.12, 0.30)
        lx = rnd.uniform(w * 0.1, w * 0.9)
        ly = rnd.uniform(h * 0.1, h * 0.9)
        stroke = c["a"] if i % 2 == 0 else c["b"]
        shapes.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="{r:.1f}" fill="none" stroke="{stroke}" stroke-width="1" opacity="0.4"/>')

    line_y = h * rnd.uniform(0.15, 0.85)
    shapes.append(f'<line x1="0" y1="{line_y:.1f}" x2="{w}" y2="{line_y - h*0.05:.1f}" stroke="{c["a"]}" stroke-width="0.6" opacity="0.25"/>')

    shapes.append(f'<rect width="{w}" height="{h}" fill="transparent" filter="url(#grain-{sid})"/>')

    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">{"".join(shapes)}</svg>'


def write(path, content):
    with open(path, "w") as f:
        f.write(content)
    print("wrote", path)


def main():
    journal_dir = os.path.join(ROOT, "assets", "journal")

    for j in JOURNAL:
        write(os.path.join(journal_dir, f"{j['slug']}.svg"), composition(1600, 1000, j, "journal"))

    hero = composition(2400, 1350, dict(slug="home-hero", bg="#FAFAF8", a="#B9BDB4", b="#D8D3C8", seed=42), "hero")
    write(os.path.join(ROOT, "assets", "hero.svg"), hero)

    portrait = composition(1000, 1200, dict(slug="portrait", bg="#F1EFEA", a="#8C9A8D", b="#C9BBA8", seed=77), "portrait")
    write(os.path.join(ROOT, "assets", "portrait.svg"), portrait)


if __name__ == "__main__":
    main()
