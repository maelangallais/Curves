# ➰ Curves
A simple interactive curve generator and editor (Bézier, Catmull-Rom & B-splines), currently playable on Numworks calculator and coded in micropython  !
#

## ⌨️ Inputs
The inputs you can do is the directional arrows to move your selected point in all directions. 

To select another point, you can press the 'OK' or 'EXE' button to cycle through all available points on the screen. The currently selected point is highlighted in blue so you always know which one you are moving.

To switch between the different curve calculations, just press the 'shift' button. It will cycle between Bézier curves, Catmull-Rom splines, and B-splines. It's so simple !
##

## 📜 Curves
The script mixes three famous curve models and lets you interact with each of them in real-time:

- **Catmull-Rom splines**: Full interpolation curve. The curve passes directly through every control point. It provides $C^1$ continuity, and the big advantage is that you have no external control handles to manage.
- **Basis splines (B-splines)**: An approximating spline curve with no interpolation, and no control handles either. The curve is at least $C^2$ continuous, which makes it very beautiful and smooth (perfect, for example, to move a camera smoothly along a path).
- **Bézier curves**: Cubic Bézier curve segments connected together with geometric continuity ($G^1$) and parametric continuity ($C^1$). Anchor points connect segments while tangent handles define the curve tension. Moving an anchor point automatically translates its handles, and moving a handle recalculates the opposite handle to preserve continuity.
##

## ℹ️ Informations
The visual markers help you easily identify every element on screen:
- **Blue point**: The currently active / selected point that you can move with the directional arrows.
- **Green points**: Anchor points on Bézier curves, or control points on Catmull-Rom and B-splines.
- **Red points**: Tangent control handles for Bézier curves.
- **Grey lines**: Collinear tangent bars linking opposite handles across Bézier junctions to visualize and maintain continuity.

The points cannot be moved outside of the screen thanks to screen boundary detection (within the 320 x 222 resolution). Each curve segment is rendered with 30 calculation steps to provide a clean and fast drawing directly on the calculator.
##

## 🖥️ Requirements
This program is coded in micropython just for Numworks calculator (using `kandinsky` and `ion` modules) but it must work on a computer if you change the module to adapt with Python (or using a Numworks simulator).
##

## 💬 Language
It was coded on a Numworks calculator in Micropython.
##

## 🛠️ Details
The project has been created the August 27 of 2024.
##
