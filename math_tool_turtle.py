import turtle
import math
import datetime

# --- INITIALIZATION & THEME ---
THEME = {
    "bg": "#0B0E14", "sidebar": "#161B22", "grid": "#1E2530",
    "btn_idle": "#21262D", "btn_active": "#58A6FF", "text": "#E0FFFF",
    "accent": "#4A6670", "label": "#F0E68C"
}
screen = turtle.Screen()

# --- THE "KILL THE WHITE BARS" PATCH ---
# 1. Removes the window border and title bar
root = screen._root
root.overrideredirect(True)

# 2. Forces the window to cover the entire screen (including taskbar)
screen.setup(width=1.0, height=1.0)

# 3. Ensures the window is centered and focused
root.focus_force()
# ---------------------------------------

screen.title("Designer Pro CAD")
screen.bgcolor(THEME["bg"])
screen.tracer(0)

app_state = {
    "category": "2D", "shape": "Rectangle", "unit": "cm",
    "val1": 15.0, "val2": 8.0, "sides": 5, "depth": 10.0,
    "color": "#2ECC71"
}

screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.title("Designer Pro CAD")
screen.bgcolor(THEME["bg"])
screen.tracer(0)

grid_t, draw_t, ui_t = turtle.Turtle(), turtle.Turtle(), turtle.Turtle()
for t in [grid_t, draw_t, ui_t]:
    t.hideturtle()
    t.penup()


def draw_grid():
    # Force recalculation of screen size to prevent black screen
    W, H = screen.window_width(), screen.window_height()
    grid_t.clear()
    grid_t.color(THEME["grid"])
    grid_t.pensize(1)

    # Draw vertical lines
    for x in range(int(-W / 2), int(W / 2), 50):
        grid_t.penup()
        grid_t.goto(x, -H / 2)
        grid_t.pendown()
        grid_t.goto(x, H / 2)
    # Draw horizontal lines
    for y in range(int(-H / 2), int(H / 2), 50):
        grid_t.penup()
        grid_t.goto(-W / 2, y)
        grid_t.pendown()
        grid_t.goto(W / 2, y)

def draw_specs(cx, cy, VIS):
    draw_t.color(THEME["label"])
    u = app_state["unit"]
    v1, v2 = app_state["val1"], app_state["val2"]
    s = app_state["shape"]

    # Moved higher to avoid overlap
    draw_t.goto(cx, cy + VIS / 2 + 130)
    if s == "Cylinder":
        txt = f"Radius: {v1}{u} | Width: {v1 * 2}{u} | Height: {v2}{u}"
    elif s == "Cuboid":
        txt = f"W: {v1}{u} | H: {v2}{u} | D: {app_state['depth']}{u}"
    elif s == "Polygon":
        txt = f"Side: {v1}{u} | Sides: {app_state['sides']}"
    elif s in ["Circle", "Sphere"]:
        txt = f"Radius: {v1}{u}"
    elif s in ["Square", "Cube"]:
        txt = f"Side: {v1}{u}"
    else:
        txt = f"Base: {v1}{u} | Height: {v2}{u}"
    draw_t.write(txt, align="center", font=("Courier", 14, "bold"))


def save_results():
    try:
        sh, u = app_state["shape"], app_state["unit"]
        filename = f"CAD_Export_{sh}.txt"
        with open(filename, "w") as f:
            f.write(f"DESIGNER PRO EXPORT\nShape: {sh}\nColor: {app_state['color']}\n")
        screen.textinput("Success", f"Saved to {filename}")
    except Exception as e:
        screen.textinput("Error", str(e))


def render_2d(s, v1, v2, u, cx, cy, VIS):
    H = screen.window_height()
    draw_t.color(app_state["color"])
    draw_t.pensize(2)
    area, perimeter, hypot = 0, 0, 0

    draw_t.begin_fill()
    if s == "Circle":
        draw_t.goto(cx, cy - VIS / 2)
        draw_t.pendown()
        draw_t.circle(VIS / 2)
        area, perimeter = math.pi * (v1 ** 2), 2 * math.pi * v1
    elif s == "Triangle":
        draw_t.goto(cx - VIS / 2, cy - VIS / 2)
        draw_t.pendown()
        draw_t.goto(cx + VIS / 2, cy - VIS / 2)
        draw_t.goto(cx, cy + VIS / 2)
        draw_t.goto(cx - VIS / 2, cy - VIS / 2)
        area, hypot = 0.5 * v1 * v2, math.sqrt((v1 / 2) ** 2 + v2 ** 2)
        perimeter = v1 + (2 * hypot)
    elif s in ["Rectangle", "Square"]:
        w_v, h_v = VIS, (VIS if s == "Square" else VIS * 0.6)
        draw_t.goto(cx - w_v / 2, cy - h_v / 2)
        draw_t.pendown()
        for _ in range(2): draw_t.forward(w_v); draw_t.left(90); draw_t.forward(h_v); draw_t.left(90)
        area, perimeter = v1 * (v1 if s == "Square" else v2), 2 * (v1 + (v1 if s == "Square" else v2))
    elif s in ["Hexagon", "Polygon"]:
        sd = 6 if s == "Hexagon" else app_state["sides"]
        angle = 360 / sd
        side_vis = (VIS * 0.7) * (2 * math.sin(math.pi / sd))
        apothem = (side_vis / 2) / math.tan(math.pi / sd)
        draw_t.penup()
        draw_t.goto(cx - side_vis / 2, cy - apothem)
        draw_t.pendown()
        for _ in range(sd): draw_t.forward(side_vis); draw_t.left(angle)
        area, perimeter = (sd * v1 ** 2) / (4 * math.tan(math.pi / sd)), sd * v1
    elif s == "Parallelogram":
        sl, hv = VIS * 0.4, VIS * 0.6
        draw_t.goto(cx - VIS / 2, cy - hv / 2)
        draw_t.pendown()
        draw_t.forward(VIS)
        draw_t.goto(cx + VIS / 2 + sl, cy + hv / 2)
        draw_t.backward(VIS)
        draw_t.goto(cx - VIS / 2, cy - hv / 2)
        area, sl_r = v1 * v2, (sl / VIS) * v1
        perimeter = 2 * (v1 + math.sqrt(v2 ** 2 + sl_r ** 2))
    draw_t.end_fill()

    draw_t.penup()
    draw_t.color(THEME["text"])
    draw_t.goto(cx, -H / 2 + 110)
    draw_t.write(f"Area: {area:.2f} {u}²", align="center", font=("Courier", 16, "bold"))
    draw_t.goto(cx, -H / 2 + 80)
    draw_t.write(f"Perimeter: {perimeter:.2f} {u}", align="center", font=("Courier", 14, "bold"))
    if s == "Triangle": draw_t.goto(cx, -H / 2 + 50); draw_t.write(f"Hypotenuse: {hypot:.2f} {u}", align="center",
                                                                   font=("Courier", 12, "italic"))


def render_3d(s, v1, v2, u, cx, cy, VIS):
    H = screen.window_height()
    FILL_COLOR, EDGE_COLOR = app_state["color"], "#008B8B"
    draw_t.color(FILL_COLOR)
    draw_t.pensize(2)
    vol = 0
    if s == "Cone":
        apex = (cx, cy + VIS / 2)
        base_y = cy - VIS / 2

        # A. Fill the Side Walls (Triangle look)
        draw_t.penup()
        draw_t.goto(cx - VIS / 2, base_y)
        draw_t.pendown()
        draw_t.color(FILL_COLOR)
        draw_t.begin_fill()
        draw_t.goto(apex)
        draw_t.goto(cx + VIS / 2, base_y)
        draw_t.goto(cx - VIS / 2, base_y)
        draw_t.end_fill()
    elif s == "Cylinder":
        # Define positions to fix "Unresolved reference"
        base_y = cy - VIS / 2
        top_y = cy + VIS / 2

        def oval_cap(y_pos, f=False):
            draw_t.penup()
            draw_t.goto(cx + VIS / 2, y_pos)
            draw_t.pendown()
            if f: draw_t.begin_fill()
            for i in range(361):
                r = math.radians(i)
                draw_t.goto(cx + (VIS / 2) * math.cos(r), y_pos + (VIS / 6) * math.sin(r))
            if f: draw_t.end_fill()

        # 1. Fill the Solid Body
        draw_t.color(FILL_COLOR)
        draw_t.penup()
        draw_t.goto(cx - VIS / 2, base_y)
        draw_t.pendown()
        draw_t.begin_fill()
        draw_t.goto(cx + VIS / 2, base_y)
        draw_t.goto(cx + VIS / 2, top_y)
        draw_t.goto(cx - VIS / 2, top_y)
        draw_t.goto(cx - VIS / 2, base_y)
        draw_t.end_fill()

        # 2. Fill Caps (Shadow for bottom, Color for top)
        draw_t.color(EDGE_COLOR)
        oval_cap(base_y, f=True)
        draw_t.color(FILL_COLOR)
        oval_cap(top_y, f=True)

        # 3. Draw Sharp Outlines
        draw_t.color(EDGE_COLOR)
        for dx in [-VIS / 2, VIS / 2]:
            draw_t.penup()
            draw_t.goto(cx + dx, base_y)
            draw_t.pendown()
            draw_t.goto(cx + dx, top_y)
        oval_cap(base_y, f=False)
        oval_cap(top_y, f=False)

        vol = math.pi * (v1 ** 2) * v2

    elif s in ["Cube", "Cuboid"]:
        wv, hv, off = VIS, (VIS if s == "Cube" else VIS * 0.6), 60
        fx, fy = cx - wv / 2, cy - hv / 2
        bx, by = fx + off, fy + off
        draw_t.color(FILL_COLOR)
        for sx, sy in [(bx, by), (fx, fy)]:
            draw_t.penup()
            draw_t.goto(sx, sy)
            draw_t.begin_fill()
            for _ in range(2): draw_t.forward(wv); draw_t.left(90); draw_t.forward(hv); draw_t.left(90)
            draw_t.end_fill()
        draw_t.begin_fill()
        draw_t.goto(fx, fy + hv)
        draw_t.goto(bx, by + hv)
        draw_t.goto(bx + wv, by + hv)
        draw_t.goto(fx + wv, fy + hv)
        draw_t.goto(fx + wv, fy)
        draw_t.goto(bx + wv, by)
        draw_t.goto(bx + wv, by + hv)
        draw_t.goto(fx + wv, fy + hv)
        draw_t.end_fill()
        draw_t.color(EDGE_COLOR)
        for sx, sy in [(fx, fy), (bx, by)]:
            draw_t.penup()
            draw_t.goto(sx, sy)
            draw_t.pendown()
            for _ in range(2): draw_t.forward(wv); draw_t.left(90); draw_t.forward(hv); draw_t.left(90)
        for dx, dy in [(0, 0), (wv, 0), (wv, hv), (0, hv)]:
            draw_t.penup()
            draw_t.goto(fx + dx, fy + dy)
            draw_t.pendown()
            draw_t.goto(bx + dx, by + dy)
        vol = v1 ** 3 if s == "Cube" else v1 * v2 * app_state["depth"]
    elif s == "Pyramid":
        # 1. Setup Coordinates
        off, apex = 60, (cx, cy + VIS / 2)
        # Corners: Front-Left, Front-Right, Back-Right, Back-Left
        c = [(cx - VIS / 2, cy - VIS / 2),
             (cx + VIS / 2, cy - VIS / 2),
             (cx + VIS / 2 + off, cy - VIS / 2 + off),
             (cx - VIS / 2 + off, cy - VIS / 2 + off)]

        # 2. Draw and Fill the Base (Darker shade)
        draw_t.penup()
        draw_t.goto(c[0])  # FIXED: Move to first point in list
        draw_t.pendown()
        draw_t.color(EDGE_COLOR)
        draw_t.begin_fill()
        for p in c:
            draw_t.goto(p)
        draw_t.goto(c[0])  # Close the loop
        draw_t.end_fill()

        # 3. Draw and Fill the 4 Triangular Faces (Cyan)
        draw_t.color(FILL_COLOR)
        for i in range(4):
            draw_t.penup()
            draw_t.goto(c[i])  # Teleport to corner to prevent "Spikes"
            draw_t.pendown()
            draw_t.begin_fill()
            draw_t.goto(apex)
            draw_t.goto(c[(i + 1) % 4])
            draw_t.goto(c[i])
            draw_t.end_fill()

        # 4. Draw Dark Outlines (Edges)
        draw_t.color(EDGE_COLOR)
        # Base Outline
        draw_t.penup();
        draw_t.goto(c[0]);
        draw_t.pendown()
        for p in c: draw_t.goto(p)
        draw_t.goto(c[0])
        # Apex Lines
        for p in c:
            draw_t.penup()
            draw_t.goto(p)
            draw_t.pendown()
            draw_t.goto(apex)

        vol = (1 / 3) * (v1 ** 2) * v2

    elif s == "Sphere":
        draw_t.penup()
        draw_t.goto(cx, cy - VIS / 2)
        draw_t.begin_fill()
        draw_t.circle(VIS / 2)
        draw_t.end_fill()
        draw_t.color(EDGE_COLOR)
        draw_t.circle(VIS / 2)
        draw_t.penup()
        draw_t.goto(cx + VIS / 2, cy)
        draw_t.pendown()
        for i in range(361):
            r = math.radians(i)
            draw_t.goto(cx + (VIS / 2) * math.cos(r), cy + (VIS / 6) * math.sin(r))
        vol = (4 / 3) * math.pi * (v1 ** 3)
    draw_t.penup()
    draw_t.color(THEME["text"])
    draw_t.goto(cx, -H / 2 + 50)
    draw_t.write(f"Volume: {vol:.2f} {u}³", align="center", font=("Courier", 18, "bold"))


def draw_ui_button(text, x, y, w, h, active):
    ui_t.penup()
    ui_t.goto(x, y)
    ui_t.color(THEME["btn_active"] if active else THEME["btn_idle"])
    ui_t.begin_fill()
    for _ in range(2): ui_t.forward(w); ui_t.left(90); ui_t.forward(h); ui_t.left(90)
    ui_t.end_fill()
    ui_t.color(THEME["text"])
    ui_t.goto(x + w / 2, y + h / 4)
    ui_t.write(text, align="center", font=("Courier", 10, "bold"))


def draw_sidebar():
    W, H = screen.window_width(), screen.window_height()
    ui_t.clear()

    # Background Panel
    ui_t.penup()
    ui_t.goto(-W / 2, -H / 2)
    ui_t.color(THEME["sidebar"])
    ui_t.begin_fill()
    for _ in range(2):
        ui_t.forward(300)
        ui_t.left(90)
        ui_t.forward(H)
        ui_t.left(90)
    ui_t.end_fill()

    # Title & Mode Buttons
    ui_t.goto(-W / 2 + 150, H / 2 - 80)
    ui_t.color(THEME["btn_active"])
    ui_t.write("DESIGNER PRO", align="center", font=("Courier", 20, "bold"))

    draw_ui_button("2D MODE", -W / 2 + 20, H / 2 - 150, 125, 40, app_state["category"] == "2D")
    draw_ui_button("3D MODE", -W / 2 + 155, H / 2 - 150, 125, 40, app_state["category"] == "3D")

    # Shape List
    shs = ["Triangle", "Circle", "Rectangle", "Square", "Hexagon", "Parallelogram", "Polygon"] if app_state[
                                                                                                      "category"] == "2D" \
        else ["Cube", "Cuboid", "Cylinder", "Pyramid", "Sphere"]
    y_off = H / 2 - 205
    for s in shs:
        draw_ui_button(s, -W / 2 + 20, y_off, 260, 32, app_state["shape"] == s)
        y_off -= 38

    # Bottom Menu
    draw_ui_button("CHANGE COLOR", -W / 2 + 20, -H / 2 + 200, 260, 45, False)
    draw_ui_button("EXPORT DATA", -W / 2 + 20, -H / 2 + 140, 260, 45, False)
    draw_ui_button("EDIT DIMENSIONS", -W / 2 + 20, -H / 2 + 80, 260, 45, False)
    draw_ui_button("EXIT", -W / 2 + 20, -H / 2 + 20, 260, 45, False)


def refresh():
    W, H = screen.window_width(), screen.window_height()
    draw_grid()
    draw_sidebar()

    draw_t.clear()
    # Center the shape in the workspace
    cx = (-W / 2 + 300 + W / 2) / 2
    draw_specs(cx, 0, 300)

    if app_state["category"] == "2D":
        render_2d(app_state["shape"], app_state["val1"], app_state["val2"], app_state["unit"], cx, 0, 300)
    else:
        render_3d(app_state["shape"], app_state["val1"], app_state["val2"], app_state["unit"], cx, 0, 300)

    # CRITICAL: This pushes all the drawing to the monitor
    screen.update()


def handle_click(x, y):
    W, H = screen.window_width(), screen.window_height()

    # --- 1. MODE SELECTION (2D vs 3D) ---
    # Detection for the 2D and 3D toggle buttons at the top
    if -W / 2 + 20 < x < -W / 2 + 145 and H / 2 - 150 < y < H / 2 - 110:
        app_state["category"], app_state["shape"], app_state["color"] = "2D", "Rectangle", "#2ECC71"
    elif -W / 2 + 155 < x < -W / 2 + 280 and H / 2 - 150 < y < H / 2 - 110:
        app_state["category"], app_state["shape"], app_state["color"] = "3D", "Cube", "#00FFFF"

    # --- 2. SIDEBAR COLUMN DETECTION ---
    elif -W / 2 + 20 < x < -W / 2 + 280:
        shs = ["Triangle", "Circle", "Rectangle", "Square", "Hexagon", "Parallelogram", "Polygon"] if app_state[
                                                                                                          "category"] == "2D" \
            else ["Cube", "Cuboid", "Cylinder", "Pyramid", "Sphere"]

        # Shape Selection Loop
        y_check = H / 2 - 205
        for s in shs:
            if y_check < y < y_check + 32:
                app_state["shape"] = s
            y_check -= 38

        # --- 3. BOTTOM MENU BUTTONS ---
        # CHANGE COLOR Button
        if -H / 2 + 200 < y < -H / 2 + 245:
            new_col = screen.textinput("Color Picker", "Enter Name or Hex:")
            if new_col:
                try:
                    ui_t.color(new_col)  # Test if valid
                    app_state["color"] = new_col
                except:
                    pass

        # EXPORT DATA Button
        elif -H / 2 + 140 < y < -H / 2 + 185:
            save_results()

        # EDIT DIMENSIONS Button
        elif -H / 2 + 80 < y < -H / 2 + 125:
            sh = app_state["shape"]
            u = app_state["unit"]

            if sh == "Cuboid":
                v1 = screen.numinput("W", f"Width ({u}):", default=app_state["val1"])
                if v1 is not None: app_state["val1"] = v1
                v2 = screen.numinput("H", f"Height ({u}):", default=app_state["val2"])
                if v2 is not None: app_state["val2"] = v2
                v3 = screen.numinput("D", f"Depth ({u}):", default=app_state["depth"])
                if v3 is not None: app_state["depth"] = v3

            elif sh in ["Circle", "Sphere", "Cylinder"]:
                v = screen.numinput("R", f"Radius ({u}):", default=app_state["val1"])
                if v is not None: app_state["val1"] = v
                if sh == "Cylinder":
                    h = screen.numinput("H", f"Height ({u}):", default=app_state["val2"])
                    if h is not None: app_state["val2"] = h

            elif sh == "Polygon":
                v1 = screen.numinput("Side", f"Length ({u}):", default=app_state["val1"])
                if v1 is not None: app_state["val1"] = v1
                v2 = screen.numinput("Sides", "Count:", default=app_state["sides"])
                if v2 is not None: app_state["sides"] = int(v2)

            else:  # Triangle, Rectangle, Parallelogram, Pyramid
                v1 = screen.numinput(sh, f"Base/Width ({u}):", default=app_state["val1"])
                if v1 is not None: app_state["val1"] = v1
                v2 = screen.numinput(sh, f"Height ({u}):", default=app_state["val2"])
                if v2 is not None: app_state["val2"] = v2

        # EXIT Button
        elif -H / 2 + 20 < y < -H / 2 + 65:
            screen.bye()
            return

    refresh()
if __name__ == "__main__":
        screen.listen()
        screen.onclick(handle_click)
        refresh()
        try:
            turtle.mainloop()
        except Exception as e:
            print(f"Window closed: {e}")
