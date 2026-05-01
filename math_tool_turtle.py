import turtle
import math
# --- CONFIGURATION & THEME ---
THEME = {
    "bg": "#0B0E14", "sidebar": "#161B22", "grid": "#1E2530",
    "btn_idle": "#21262D", "btn_active": "#58A6FF", "text": "#E0FFFF",
    "accent": "#4A6670", "label": "#F0E68C"
}

app_state = {
    "category": "2D", "shape": "Rectangle", "unit": "cm",
    "val1": 15.0, "val2": 8.0, "sides": 5
}

# --- INITIALIZATION ---
screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.title("Designer Pro CAD")
screen.bgcolor(THEME["bg"])
screen.tracer(0)

# Layered Turtles for performance
grid_t, draw_t, ui_t = turtle.Turtle(), turtle.Turtle(), turtle.Turtle()
for t in [grid_t, draw_t, ui_t]:
    t.hideturtle()
    t.penup()


def draw_grid():
    grid_t.clear()
    grid_t.color(THEME["grid"])
    for x in range(-350, 1000, 50):
        grid_t.goto(x, -600)
        grid_t.pendown()
        grid_t.goto(x, 600)
        grid_t.penup()
    for y in range(-600, 600, 50):
        grid_t.goto(-350, y)
        grid_t.pendown()
        grid_t.goto(1000, y)
        grid_t.penup()


def draw_specs(cx, cy, VIS):
    draw_t.color(THEME["label"])
    draw_t.goto(cx - VIS / 2, cy + VIS / 2 + 20)
    s = app_state["shape"]
    u = app_state["unit"]
    v1, v2 = app_state["val1"], app_state["val2"]

    if s == "Parallelogram":
        # Calculate the actual length of the tilted side
        slant_dist = VIS * 0.4  # This matches the slant in the drawing engine
        # Map the visual slant back to the real-world scale
        real_slant_offset = (slant_dist / VIS) * v1
        actual_slant = math.sqrt(v2 ** 2 + real_slant_offset ** 2)
        txt = f"Base: {v1}{u} | Height: {v2}{u} | Slant: {actual_slant:.1f}{u}"
    elif s in ["Circle", "Sphere"]:
        txt = f"Radius: {v1}{u}"
    elif s in ["Square", "Cube"]:
        txt = f"Side: {v1}{u}"
    elif s == "Polygon":
        txt = f"Side: {v1}{u} | Sides: {app_state['sides']}"
    else:
        txt = f"Base: {v1}{u} | Height: {v2}{u}"

    draw_t.write(txt, font=("Courier", 14, "italic"))


def render_2d(s, v1, v2, u, cx, cy, VIS):
    draw_t.color(THEME["text"])
    draw_t.pensize(2)

    if s == "Circle":
        draw_t.goto(cx, cy - VIS / 2)
        draw_t.pendown()
        draw_t.circle(VIS / 2)
        draw_t.penup()
        area = math.pi * (v1 ** 2)
    elif s == "Triangle":
        draw_t.goto(cx - VIS / 2, cy - VIS / 2)
        draw_t.pendown()
        draw_t.goto(cx + VIS / 2, cy - VIS / 2)
        draw_t.goto(cx, cy + VIS / 2)
        draw_t.goto(cx - VIS / 2, cy - VIS / 2)
        draw_t.penup()
        area = 0.5 * v1 * v2
    elif s in ["Rectangle", "Square"]:
        w, h = VIS, (VIS if s == "Square" else VIS * 0.6)
        draw_t.goto(cx - w / 2, cy - h / 2)
        draw_t.pendown()
        for _ in range(2): draw_t.forward(w); draw_t.left(90); draw_t.forward(h); draw_t.left(90)
        draw_t.penup()
        area = v1 * (v1 if s == "Square" else v2)
    elif s == "Hexagon" or s == "Polygon":
        sides = 6 if s == "Hexagon" else app_state["sides"]
        angle = 360 / sides
        draw_t.goto(cx, cy - VIS / 2)
        draw_t.pendown()
        for _ in range(sides): draw_t.forward(VIS * (2 * math.sin(math.pi / sides))); draw_t.left(angle)
        draw_t.penup()
        area = (sides * v1 ** 2) / (4 * math.tan(math.pi / sides))
    elif s == "Parallelogram":
        # 1. VISUAL SETUP
        slant_offset = VIS * 0.4  # Horizontal lean
        h_vis = VIS * 0.6  # Visual height on screen

        # 2. DRAWING LOGIC
        draw_t.goto(cx - VIS / 2, cy - h_vis / 2)  # Start bottom-left
        draw_t.pendown()
        draw_t.forward(VIS)  # Bottom Base
        draw_t.goto(cx + VIS / 2 + slant_offset, cy + h_vis / 2)  # Right Slant
        draw_t.backward(VIS)  # Top Base
        draw_t.goto(cx - VIS / 2, cy - h_vis / 2)  # Left Slant
        draw_t.penup()

        # 3. MATH FOR LABELS
        # Calculate the actual length of the slanted side using Pythagoras
        # We convert the visual pixels back to the user's scale
        real_slant_x = (slant_offset / VIS) * v1
        actual_slant_len = math.sqrt(v2 ** 2 + real_slant_x ** 2)

        # 4. AREA AND PERIMETER LABELS
        area = v1 * v2
        perimeter = 2 * (v1 + actual_slant_len)

        draw_t.goto(cx, -VIS / 2 - 80)
        draw_t.write(f"Area: {area:.2f} {u}²", align="center", font=("Courier", 18, "bold"))
        draw_t.goto(cx, -VIS / 2 - 110)
        draw_t.write(f"Perimeter: {perimeter:.2f} {u}", align="center", font=("Courier", 14, "bold"))


def render_3d(s, v1, v2, u, cx, cy, VIS):
    draw_t.pensize(2)

    if s == "Cylinder":
        def oval(y, c):
            draw_t.penup()
            draw_t.goto(cx + VIS / 2, cy + y)
            draw_t.pendown()
            draw_t.color(c)
            for i in range(361):
                r = math.radians(i)
                draw_t.goto(cx + (VIS / 2) * math.cos(r), (cy + y) + (VIS / 6) * math.sin(r))

        oval(-VIS / 2, THEME["accent"])
        oval(VIS / 2, THEME["text"])
        draw_t.color(THEME["text"])
        for dx in [-VIS / 2, VIS / 2]:
            draw_t.goto(cx + dx, cy - VIS / 2)
            draw_t.pendown()
            draw_t.goto(cx + dx, cy + VIS / 2)
            draw_t.penup()
        vol = math.pi * (v1 ** 2) * v2
    elif s == "Pyramid":
        off = 60
        apex = (cx, cy + VIS / 2)
        corners = [(cx - VIS / 2, cy - VIS / 2), (cx + VIS / 2, cy - VIS / 2), (cx + VIS / 2 + off, cy - VIS / 2 + off),
                   (cx - VIS / 2 + off, cy - VIS / 2 + off)]
        draw_t.color(THEME["accent"])
        draw_t.goto(corners[-1])
        draw_t.pendown()
        for p in corners: draw_t.goto(p)
        draw_t.penup()
        draw_t.color(THEME["text"])
        for p in corners: draw_t.goto(p); draw_t.pendown(); draw_t.goto(apex); draw_t.penup()
        vol = (1 / 3) * (v1 ** 2) * v2
    elif s == "Sphere":
        draw_t.color(THEME["text"])
        draw_t.goto(cx, cy - VIS / 2)
        draw_t.pendown()
        draw_t.circle(VIS / 2)
        draw_t.penup()
        draw_t.color(THEME["accent"])
        draw_t.goto(cx + VIS / 2, cy)
        draw_t.pendown()
        for i in range(361):
            r = math.radians(i)
            draw_t.goto(cx + (VIS / 2) * math.cos(r), cy + (VIS / 6) * math.sin(r))
        draw_t.penup()
        vol = (4 / 3) * math.pi * (v1 ** 3)
    elif s == "Cube":
        off = 70

        def box(x, y, c):
            draw_t.goto(x, y)
            draw_t.pendown()
            draw_t.color(c)
            for _ in range(4): draw_t.forward(VIS); draw_t.left(90)
            draw_t.penup()

        box(cx - VIS / 2 + off, cy - VIS / 2 + off, THEME["accent"])
        box(cx - VIS / 2, cy - VIS / 2, THEME["text"])
        for dx, dy in [(-VIS / 2, -VIS / 2), (VIS / 2, -VIS / 2), (VIS / 2, VIS / 2), (-VIS / 2, VIS / 2)]:
            draw_t.goto(cx + dx, cy + dy)
            draw_t.pendown()
            draw_t.goto(cx + dx + off, cy + dy + off)
            draw_t.penup()
        vol = v1 ** 3

    draw_t.color(THEME["text"])
    draw_t.goto(cx, -VIS / 2 - 100)
    draw_t.write(f"Volume: {vol:.2f} {u}³", align="center", font=("Courier", 18, "bold"))


def draw_ui_button(text, x, y, w, h, active):
    ui_t.goto(x, y)
    ui_t.color(THEME["btn_active"] if active else THEME["btn_idle"])
    ui_t.begin_fill()
    for _ in range(2): ui_t.forward(w); ui_t.left(90); ui_t.forward(h); ui_t.left(90)
    ui_t.end_fill()
    ui_t.color(THEME["text"])
    ui_t.goto(x + w / 2, y + h / 4)
    ui_t.write(text, align="center", font=("Courier", 11, "bold"))


def draw_sidebar():
    ui_t.clear()
    ui_t.goto(-700, -600)
    ui_t.color(THEME["sidebar"])
    ui_t.begin_fill()
    for _ in range(2): ui_t.forward(300); ui_t.left(90); ui_t.forward(1200); ui_t.left(90)
    ui_t.end_fill()
    ui_t.goto(-550, 400)
    ui_t.color(THEME["btn_active"])
    ui_t.write("DESIGNER PRO", align="center", font=("Courier", 22, "bold"))

    draw_ui_button("2D MODE", -680, 340, 125, 40, app_state["category"] == "2D")
    draw_ui_button("3D MODE", -545, 340, 125, 40, app_state["category"] == "3D")

    shapes = ["Triangle", "Circle", "Rectangle", "Square", "Hexagon", "Parallelogram", "Polygon"] if app_state["category"] == "2D" else [
        "Cube", "Cylinder", "Pyramid", "Sphere"]
    y = 280
    for s in shapes:
        draw_ui_button(s, -680, y, 260, 35, app_state["shape"] == s)
        y -= 45
    draw_ui_button("EDIT DIMENSIONS", -680, -350, 260, 45, False)
    draw_ui_button("EXIT", -680, -410, 260, 45, False)


def refresh():
    draw_sidebar()
    draw_t.clear()
    cx, cy, VIS = 200, 0, 300
    draw_specs(cx, cy, VIS)
    if app_state["category"] == "2D":
        render_2d(app_state["shape"], app_state["val1"], app_state["val2"], app_state["unit"], cx, cy, VIS)
    else:
        render_3d(app_state["shape"], app_state["val1"], app_state["val2"], app_state["unit"], cx, cy, VIS)
    screen.update()


def handle_click(x, y):
    if -680 < x < -555 and 340 < y < 380:
        app_state["category"] = "2D"; app_state["shape"] = "Rectangle"
    elif -545 < x < -420 and 340 < y < 380:
        app_state["category"] = "3D"; app_state["shape"] = "Cube"
    elif -680 < x < -420:
        shapes = ["Triangle", "Circle", "Rectangle", "Square", "Hexagon","Parallelogram", "Polygon"] if app_state[
                                                                                            "category"] == "2D" else [
            "Cube", "Cylinder", "Pyramid", "Sphere"]
        y_btn = 280
        for s in shapes:
            if y_btn < y < y_btn + 35: app_state["shape"] = s
            y_btn -= 45
        if -350 < y < -305:
            sh = app_state["shape"]
            if sh in ["Circle", "Sphere"]:
                v = screen.numinput("Edit", "Enter Radius:", default=app_state["val1"])
                if v: app_state["val1"] = v
            elif sh in ["Square", "Cube"]:
                v = screen.numinput("Edit", "Enter Side Length:", default=app_state["val1"])
                if v: app_state["val1"] = v
            elif sh == "Polygon":
                v1 = screen.numinput("Edit", "Enter Side Length:", default=app_state["val1"])
                v2 = screen.numinput("Edit", "Number of Sides:", default=app_state["sides"])
                if v1: app_state["val1"] = v1
                if v2: app_state["sides"] = int(v2)
            else:
                v1 = screen.numinput("Edit", "Enter Base/Width:", default=app_state["val1"])
                v2 = screen.numinput("Edit", "Enter Height:", default=app_state["val2"])
                if v1: app_state["val1"] = v1
                if v2: app_state["val2"] = v2
        if -410 < y < -365: screen.bye()
    refresh()


draw_grid()
refresh()
screen.onclick(handle_click)
screen.listen()
turtle.done()
