#!/usr/bin/env python3
"""Draws the three 'design concept' illustrations (basement, garage, office)
as SVG files in images/. They are drawings, not photos, so no one can mistake
them for finished client work.

Run from the repo root:  python3 .github/scripts/make_concepts.py
"""

W, H = 1200, 800
# One-point perspective room: back wall rectangle, floor/ceiling/side walls
# run out to the frame edges.
BX0, BY0, BX1, BY1 = 330, 170, 870, 520   # back wall


def poly(pts, fill, extra=''):
    return f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="{fill}" {extra}/>'


def lerp(a, b, t):
    return a + (b - a) * t


def floor_pt(u, v):
    """u: 0 left..1 right across the floor, v: 0 back wall..1 front edge."""
    xl, xr = lerp(BX0, 0, v), lerp(BX1, W, v)
    return lerp(xl, xr, u), lerp(BY1, H, v)


def room(p):
    s = []
    s.append(poly([(0, 0), (W, 0), (BX1, BY0), (BX0, BY0)], p['ceiling']))
    s.append(poly([(0, 0), (BX0, BY0), (BX0, BY1), (0, H)], p['wall_l']))
    s.append(poly([(W, 0), (BX1, BY0), (BX1, BY1), (W, H)], p['wall_r']))
    s.append(poly([(BX0, BY1), (BX1, BY1), (W, H), (0, H)], p['floor']))
    s.append(f'<rect x="{BX0}" y="{BY0}" width="{BX1-BX0}" height="{BY1-BY0}" fill="{p["back"]}"/>')
    # Floor boards / texture lines
    for i in range(1, 9):
        u = i / 9
        x0, y0 = floor_pt(u, 0)
        x1, y1 = floor_pt(u, 1)
        s.append(f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y1:.0f}" stroke="{p["floor_line"]}" stroke-width="2"/>')
    # Ceiling lights
    for u in (0.3, 0.7):
        for v in (0.35, 0.7):
            x = lerp(lerp(BX0, 0, v), lerp(BX1, W, v), u)
            y = lerp(BY0, 0, v)
            r = lerp(7, 16, v)
            s.append(f'<ellipse cx="{x:.0f}" cy="{y+10:.0f}" rx="{r*1.6:.0f}" ry="{r*0.5:.0f}" fill="#FFF4D6" opacity=".9"/>')
    return s


def screen():
    # Impact screen with a fairway scene, plus turf hitting area in front.
    sx0, sy0, sx1, sy1 = BX0 + 60, BY0 + 30, BX1 - 60, BY1 - 20
    w, h = sx1 - sx0, sy1 - sy0
    s = [f'<rect x="{sx0-8}" y="{sy0-8}" width="{w+16}" height="{h+16}" fill="#111" rx="3"/>',
         '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#7FB6E0"/><stop offset="1" stop-color="#D9ECF7"/></linearGradient>'
         '<clipPath id="scr"><rect x="%d" y="%d" width="%d" height="%d"/></clipPath></defs>' % (sx0, sy0, w, h),
         f'<g clip-path="url(#scr)">',
         f'<rect x="{sx0}" y="{sy0}" width="{w}" height="{h}" fill="url(#sky)"/>',
         f'<path d="M{sx0} {sy0+h*.55} Q{sx0+w*.25} {sy0+h*.35} {sx0+w*.45} {sy0+h*.5} T{sx1} {sy0+h*.45} V{sy1} H{sx0}Z" fill="#6E9A62"/>',
         f'<path d="M{sx0} {sy0+h*.68} Q{sx0+w*.5} {sy0+h*.58} {sx1} {sy0+h*.66} V{sy1} H{sx0}Z" fill="#4E8A45"/>',
         f'<path d="M{sx0+w*.42} {sy1} L{sx0+w*.49} {sy0+h*.62} L{sx0+w*.53} {sy0+h*.62} L{sx0+w*.62} {sy1}Z" fill="#7DBA5E"/>',
         f'<line x1="{sx0+w*.52}" y1="{sy0+h*.62}" x2="{sx0+w*.52}" y2="{sy0+h*.5}" stroke="#fff" stroke-width="2"/>',
         f'<polygon points="{sx0+w*.52},{sy0+h*.5} {sx0+w*.56},{sy0+h*.52} {sx0+w*.52},{sy0+h*.54}" fill="#D9473B"/>',
         f'<path d="M{sx0+w*.5} {sy1-6} Q{sx0+w*.47} {sy0+h*.2} {sx0+w*.52} {sy0+h*.58}" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="4 5" opacity=".8"/>',
         '</g>']
    # Turf strip from the screen to the front
    a, b = floor_pt(0.28, 0), floor_pt(0.72, 0)
    c, d = floor_pt(0.72, 0.62), floor_pt(0.28, 0.62)
    s.append(poly([a, b, c, d], '#3F7A3E'))
    # Hitting mat
    a, b = floor_pt(0.42, 0.42), floor_pt(0.58, 0.42)
    c, d = floor_pt(0.58, 0.56), floor_pt(0.42, 0.56)
    s.append(poly([a, b, c, d], '#5FA058'))
    tx, ty = floor_pt(0.5, 0.48)
    s.append(f'<circle cx="{tx:.0f}" cy="{ty:.0f}" r="5" fill="#fff"/>')
    # Launch monitor box beside the mat
    mx, my = floor_pt(0.62, 0.5)
    s.append(f'<rect x="{mx:.0f}" y="{my-22:.0f}" width="34" height="24" rx="3" fill="#222"/><rect x="{mx+6:.0f}" y="{my-16:.0f}" width="22" height="10" rx="2" fill="#3A6EA5"/>')
    # Ceiling projector
    px, py = (BX0 + BX1) / 2, 70
    s.append(f'<rect x="{px-6}" y="0" width="12" height="{py-12}" fill="#333"/><rect x="{px-40}" y="{py-14}" width="80" height="28" rx="5" fill="#2A2A2A"/><circle cx="{px}" cy="{py+1}" r="7" fill="#556"/>')
    return s


def basement():
    p = dict(ceiling='#E9E3D6', wall_l='#2C4A4F', wall_r='#24403F', back='#1E3437', floor='#9A7350', floor_line='#87633F')
    s = room(p) + screen()
    # Sectional sofa at front right
    s.append('<path d="M760 640 h300 v110 h-300z" fill="#6B7F5E"/><path d="M760 610 h300 v40 h-300z" fill="#7C9170"/><path d="M1040 560 h80 v190 h-80z" fill="#6B7F5E"/>')
    # Side table and lamp
    s.append('<rect x="660" y="690" width="70" height="60" fill="#5A3E28"/><rect x="690" y="640" width="8" height="50" fill="#333"/><path d="M670 615 h48 l-10 28 h-28z" fill="#F2E3B5"/>')
    # Framed art on left wall
    s.append(poly([(110, 250), (200, 270), (200, 360), (110, 350)], '#C9B48A') + poly([(120, 262), (190, 278), (190, 350), (120, 340)], '#3E6B54'))
    # Club rack on left wall
    for i in range(5):
        x = 230 + i * 14
        s.append(f'<line x1="{x}" y1="{420+i*3}" x2="{x+6}" y2="{560+i*6}" stroke="#BBB" stroke-width="4"/>')
    return s


def garage():
    p = dict(ceiling='#D7D9DB', wall_l='#C9CDD1', wall_r='#BFC4C8', back='#A9B0B6', floor='#8E9399', floor_line='#7E8389')
    s = room(p)
    # Garage-door tracks along the ceiling
    for x0, x1 in ((BX0 + 20, 40), (BX1 - 20, W - 40)):
        s.append(f'<line x1="{x0}" y1="{BY0+4}" x2="{x1}" y2="20" stroke="#6B7075" stroke-width="5"/>')
    s += screen()
    # Retractable screen housing above the screen
    s.append(f'<rect x="{BX0+40}" y="{BY0+6}" width="{BX1-BX0-80}" height="16" rx="4" fill="#3B3F43"/>')
    # Wall-mounted pegboard and workbench at left
    s.append(poly([(60, 300), (240, 330), (240, 470), (60, 460)], '#B88E5C'))
    for i in range(6):
        for j in range(4):
            s.append(f'<circle cx="{80+i*28}" cy="{320+j*34+i*4}" r="2" fill="#7D5E3A"/>')
    s.append(poly([(40, 520), (260, 540), (260, 570), (40, 560)], '#6E4D2E'))
    # Bar stools at front left
    for x in (120, 260):
        s.append(f'<rect x="{x}" y="660" width="70" height="14" rx="6" fill="#222"/><line x1="{x+35}" y1="674" x2="{x+35}" y2="780" stroke="#555" stroke-width="6"/>')
    # Rolling tool chest at right
    s.append('<rect x="980" y="560" width="140" height="190" rx="6" fill="#B2312B"/>' + ''.join(f'<rect x="992" y="{575+i*34}" width="116" height="24" rx="3" fill="#C9433B"/>' for i in range(5)))
    return s


def office():
    p = dict(ceiling='#EEECE7', wall_l='#E4E1DA', wall_r='#DCD8D0', back='#15302F', floor='#B79466', floor_line='#A6845A')
    s = room(p) + screen()
    # Glass wall on right with mullions
    s.append(poly([(BX1, BY0), (W, 0), (W, H), (BX1, BY1)], '#BFD7DF', 'opacity=".55"'))
    for t in (0.25, 0.5, 0.75):
        x = lerp(BX1, W, t)
        s.append(f'<line x1="{x:.0f}" y1="{lerp(BY0,0,t):.0f}" x2="{x:.0f}" y2="{lerp(BY1,H,t):.0f}" stroke="#8FA9B2" stroke-width="3"/>')
    # Lounge chairs front
    for x in (90, 300):
        s.append(f'<path d="M{x} 640 q90 -50 180 0 v110 h-180z" fill="#2F5D50"/><rect x="{x+15}" y="690" width="150" height="40" rx="10" fill="#3C7263"/>')
    # TV and logo wall on left
    s.append(poly([(70, 230), (230, 262), (230, 360), (70, 340)], '#1A1A1A') + poly([(80, 242), (220, 270), (220, 350), (80, 330)], '#2B5876'))
    # Coffee table
    s.append('<ellipse cx="760" cy="720" rx="120" ry="28" fill="#4A3524"/>')
    return s


SCENES = {
    'concept-basement': (basement, 'Design concept: basement golf simulator room'),
    'concept-garage': (garage, 'Design concept: garage golf simulator with retractable screen'),
    'concept-office': (office, 'Design concept: office or commercial golf simulator lounge'),
}

if __name__ == '__main__':
    for name, (fn, title) in SCENES.items():
        body = '\n'.join(fn())
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">'
               f'<title>{title}</title>\n{body}\n</svg>\n')
        with open(f'images/{name}.svg', 'w') as fh:
            fh.write(svg)
        print('wrote', name)
