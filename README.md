# ➰ Curves

A simple interactive curve generator and editor (Bézier, Catmull-Rom & B-splines), currently playable on NumWorks calculator and coded in MicroPython!

---

## ⌨️ Inputs

- **Directional Arrows** : Move the currently selected point in all directions.
- **OK / EXE** : Cycle through all available points on the screen. The active point is highlighted in **blue**.
- **Shift** : Switch between curve calculation engines in real-time (**Bézier curves**, **Catmull-Rom splines**, and **B-splines**).

---

## 📜 Curve Models

The final script combines three classic mathematical curves:

- **Catmull-Rom splines**: Full interpolation curve. The curve passes directly through every control point. It provides $C^1$ continuity, with no external control handles to manage.
- **Basis splines (B-splines)**: An approximating spline curve with no interpolation and no control handles. The curve is at least $C^2$ continuous, ensuring a smooth trajectory (ideal for camera paths).
- **Bézier curves**: Cubic Bézier segments connected together with geometric continuity ($G^1$) and parametric continuity ($C^1$). Anchor points connect segments while tangent handles define curve tension. Moving an anchor point automatically translates its handles, and moving a handle recalculates the opposite handle to preserve continuity.

---

## ℹ️ Visual Elements

- **Blue point**: Active / selected point movable with the arrows.
- **Green points**: Anchor points (Bézier) or control points (Catmull-Rom / B-splines).
- **Red points**: Tangent control handles for Bézier curves.
- **Grey lines**: Collinear tangent bars linking opposite handles across Bézier junctions to maintain continuity.

*Points are clamped within the native 320 × 222 screen resolution. Each segment is rendered with 30 calculation steps for real-time smoothness.*

---

## 🕰️ Project Evolution & History

Previous iterations and milestones are preserved in the [`history/`](history/) folder:

1. **`bezier_curves_v1.py`** *(Created July 09, 2024)* : Initial prototype drawing quadratic Bézier curves with 3 to 4 interactive points.
2. **`bezier_curves_v2.py`** *(Created August 16, 2024)* : Algorithmic optimization with reduced complexity using a linear interpolation (`lerp`) approach.
3. **`bezier_curves_v3.py`** *(Created August 16, 2024)* : Introduced $G^1$ constraint locking between control points to prevent sharp corner artifacts.
4. **`bezier_curves_v4.py`** *(Created August 26, 2024)* : Mirrored control handles and reworked curve calculation engine for multi-segment flexibility.
5. **`bezier_curves_final.py`** *(Created August 26, 2024)* : Multi-curve playground integrating dynamic point manipulation.
6. **`curves.py`** *(Created August 27, 2024)* : Complete release mixing Bézier, Catmull-Rom ($C^1$) and B-splines ($C^2$) with live mode switching (`Shift`).

---

## 🖥️ Requirements & Environment

- Coded in **MicroPython** specifically for the **NumWorks** calculator.
- Uses `kandinsky` (graphics) and `ion` (keyboard inputs).
- Also runs seamlessly inside NumWorks simulators or on desktop Python with compatible mocks.
