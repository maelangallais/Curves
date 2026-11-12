# Créé le 27 Août 2024
# Interactive Curve Generator & Editor for NumWorks (MicroPython)
# Supports Bézier curves, Catmull-Rom splines, and B-splines (Basis splines)

from math import pi, sin, cos, fabs as va, floor
from kandinsky import fill_rect as fr
from ion import keydown as kd
from time import sleep as sl

# Color definitions (RGB tuples)
bk, wh = (0,) * 3, (255,) * 3                        # Black (lines), White (background)
re, gr, bl = (255, 0, 0), (0, 255, 0), (0, 0, 255)  # Red (handles), Green (anchors), Blue (selected)

# Control points configuration for each curve type
# 1. Cubic Bézier curves (closed loop of 4 segments with 12 control points)
value1 = [
  (270, 110), (310, 10), (180, 20),
  (160, 60), (140, 20), (10, 10),
  (50, 110), (60, 150), (130, 160),
  (160, 200), (190, 160), (260, 150)
] # For bezier curves

# 2. Catmull-Rom spline (9 control points with full interpolation)
value2 = [
  (20, 20), (130, 30), (60, 60),
  (40, 190), (110, 120), (160, 200),
  (300, 100), (180, 150), (210, 70)
] # For Catmull-Rom

# 3. Uniform B-splines (6 control points, C2 continuous smooth approximation)
value3 = [
  (20, 200), (20, 20), (160, 20),
  (160, 200), (300, 200), (300, 20)
] # For b-splines

# Segment connectivity: which sets of 4 control points define each cubic Bézier segment
# Links and continuity are only for bezier curves
links = [[0, 1, 2, 3], [3, 4, 5, 6], [6, 7, 8, 9], [9, 10, 11, 0]]  # Quels points sont reliés entre eux

# Continuity constraints between connected Bézier segments:
# (handle_prev, anchor, handle_next, continuity_type)
# continuity_type: 1 = G1 (geometric: tangent directions aligned); 2 = C1 (parametric: matching direction & magnitude)
ct = [(11, 0, 1, 1), (5, 6, 7, 1)]  # Continuity: 1=G1; 2=C1

step = 30  # Nombre d'étapes pour dessiner la courbe (interpolation precision)
wc = 1     # Which Curve (1=bezier; 2=catmull; 3=basis)

value = eval("value" + str(wc))  # Active points list
fp = [v[0] for v in links]       # First Points (Anchor Points of Bézier curves: 0, 3, 6, 9)
wv = 0                           # Which value (index of currently selected point)
dm = 3                           # Valeur du déplacement de la sélection (pixel step per movement)
width, height = 320, 222         # NumWorks calculator screen dimensions
cr = 3                           # Taille du cercle (control point display radius)

# Utility lambdas
inf = lambda x1, x2: x1 < x2
sup = lambda x1, x2: x1 > x2
ent = lambda n: floor(n) if n - floor(n) < 0.5 else floor(n) + 1  # Rounding helper
dst = lambda x1, y1, x2, y2: ((x1 - x2)**2 + (y1 - y2)**2)**.5   # Euclidean distance

def draw_point(cx, cy, cl):
  """Draws a filled circle centered at (cx, cy) with radius cr and color cl."""
  for rep in range(int(8 * cr * pi)):
    adj = cos(rep) * cr
    x = cx + adj
    opp = sin(rep) * cr
    y = cy + opp
    fr(ent(x), ent(y), 1, -2 * ent(opp), cl)

def draw_points():
  """Renders all control points for the active curve mode."""
  for i in range(len(value)):
    if wc == 1:
      # Blue for selected, Green for anchor points, Red for tangent handles
      cl = bl if i == wv else gr if i in fp else re
    else:
      # Blue for selected, Green for all other curve points
      cl = bl if i == wv else gr
    draw_point(value[i][0], value[i][1], cl)

def dl(x1, y1, x2, y2, t=1, cl=bk):
  """Draws a line between (x1, y1) and (x2, y2) with thickness t and color cl."""
  w = h = 1
  dx = min(max((x2 - x1) / va(y2 - y1) if va(y2 - y1) != 0 else x2 - x1, -1), 1)
  dy = min(max((y2 - y1) / va(x2 - x1) if va(x2 - x1) != 0 else y2 - y1, -1), 1)
  c = va(x2 - x1) if va(x2 - x1) > va(y2 - y1) else va(y2 - y1)
  if va(dx) < va(dy):
    w, x1, x2 = t, x1 - (t - 1) // 2, x2 - (t - 1) // 2
  else:
    h, y1, y2 = t, y1 - (t - 1) // 2, y2 - (t - 1) // 2
  for i in range(int(c)):
    fr(ent(x1 + dx * i), ent(y1 + dy * i), w, h, cl)

def ft(l, t):
  """FuncTion to calculate the curve point at parameter t in [0, 1] given 4 control values [a, b, c, d]."""
  [a, b, c, d] = [v for v in l]
  if wc == 1:
    # Cubic Bézier formula
    return (1 - t)**3 * a + 3 * (1 - t)**2 * t * b + 3 * (1 - t) * t**2 * c + t**3 * d
  elif wc == 2:
    # Catmull-Rom spline formula (C1 continuous, interpolating all points)
    return (1 / 2) * ((-a + 3 * b - 3 * c + d) * t**3 + (2 * a - 5 * b + 4 * c - d) * t**2 + (-a + c) * t + (2 * b))
  elif wc == 3:
    # Uniform cubic B-spline formula (C2 continuous, smooth non-interpolating approximation)
    return (1 / 6) * ((-a + 3 * b - 3 * c + d) * t**3 + (3 * a - 6 * b + 3 * c) * t**2 + (-3 * a + 3 * c) * t + (a + 4 * b + c))

def draw_curve(val):
  """Draws a curve segment defined by 4 control points using step subdivisions."""
  x, y = [], []
  for i in range(step + 1):
    t = 1 / step * i
    x.append(ft([v[0] for v in val], t))
    y.append(ft([v[1] for v in val], t))
  for i in range(step):
    dl(ent(x[i]), ent(y[i]), ent(x[i + 1]), ent(y[i + 1]), 3)

def c_v(a, b, c, lr):
  """
  Calculate (new) Values: updates position of handle 'c' relative to anchor 'b' and handle 'a'.
  lr = 1: G1 geometric continuity (preserves handle 'c' length while aligning tangent direction)
  lr = 2: C1 parametric continuity (matches handle 'a' length and aligns tangent direction)
  """
  v1, v2, v3 = value[a], value[b], value[c]
  x1, y1, x2, y2, x3, y3 = v1[0], v1[1], v2[0], v2[1], v3[0], v3[1]
  r1, r2 = dst(x1, y1, x2, y2), dst(x3, y3, x2, y2)
  dx, dy = (va(x1 - x2) / r1) * (1 if x2 >= x1 else -1), (va(y1 - y2) / r1) * (1 if y2 >= y1 else -1)
  rd = r1 if lr - 1 else r2  # Lock Rotation / Length
  nx, ny = x2 + dx * rd, y2 + dy * rd
  value[c] = (ent(nx), ent(ny))

def move(i, n):
  """Moves point index n according to direction i (0: Left, 1: Up, 2: Down, 3: Right)."""
  vl = value[n]
  xv = vl[0] - dm if i == 0 else vl[0] + dm if i == 3 else vl[0]
  yv = vl[1] - dm if i == 1 else vl[1] + dm if i == 2 else vl[1]
  value[n] = (xv, yv)

new = True
# Initial alignment of Bézier continuity handles
if wc == 1:
  for v in ct:
    c_v(v[0], v[1], v[2], v[3])

# Main interactive loop
while True:
  if new:
    new = False
    fr(0, 0, 320, 222, wh)  # Clear screen to white
    if wc == 1:
      # Draw Bézier segments
      for link in links:
        draw_curve([value[i] for i in link])
      # Draw tangent constraint lines in grey between opposite handles
      for v in ct:
        dl(value[v[0]][0], value[v[0]][1], value[v[2]][0], value[v[2]][1], 1, (120,) * 3)
    else:
      # Complete interpolation for Catmull-Rom and B-splines
      for i in range(-wc + 1, len(value) - 4 + wc):
        draw_curve([value[min(max(0, i + n), len(value) - 1)] for n in range(4)])
    draw_points()

  # Directional pad handling (0: Left, 1: Up, 2: Down, 3: Right)
  for i in range(4):
    if kd(i):
      vl = value[wv]
      # Boundary check: keep points inside the 320x222 screen
      for n in range(4):
        f, v1, v2 = inf if n < 2 else sup, 1 if n in [1, 2] else 0, height if n == 2 else width if n == 3 else 0
        if i == n and f(vl[v1], v2):
          n = 5
          break
      if n == 5:
        continue
      move(i, wv)
      new = True
      if not wc == 1:
        continue
      # Bézier continuity management: update linked handles and anchors dynamically
      for v in ct:
        a, b, c, d = v[0], v[1], v[2], v[3]
        if wv == a:
          c_v(a, b, c, d)  # Handle 'a' moved -> update opposite handle 'c'
        if wv == b:
          move(i, a); move(i, c)  # Anchor 'b' moved -> translate attached handles
        if wv == c:
          c_v(c, b, a, d)  # Handle 'c' moved -> update opposite handle 'a'

  # Cycle through points using 'OK' (key 4) or 'EXE' (key 52)
  if kd(4) or kd(52):
    wv = wv + 1 if wv < len(value) - 1 else 0
    draw_points()
    sl(0.1)

  # Switch curve type using 'shift' (key 12): 1 (Bézier) -> 2 (Catmull-Rom) -> 3 (B-spline)
  if kd(12):
    wc, wv = wc + 1 if wc < 3 else 1, 0
    value = eval("value" + str(wc))
    new = True
    sl(0.1)
