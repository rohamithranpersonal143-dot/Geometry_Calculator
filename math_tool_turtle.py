import turtle
import math
if __name__ == "__main__":
    THEME = {
        "bg": "#0B0E14", "sidebar": "#161B22", "grid": "#1E2530",
        "btn_idle": "#21262D", "btn_active": "#58A6FF", "text": "#E0FFFF",
        "accent": "#4A6670", "label": "#F0E68C"
    }

    app_state = {
        "category": "2D",
        "shape": "Rectangle",
        "unit": "cm",
        "val1": 15.0,
        "val2": 8.0,
        "sides": 5,
        "color": "#2ECC71"
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
        draw_t.clear()
        # Pull color from app_state; default to light blue if not set
        current_color = app_state.get("color", "#E0FFFF")
        draw_t.color(current_color)
        draw_t.pensize(2)

        area = 0
        perimeter = 0
        hypot = 0

        # --- START DRAWING & FILL ---
        draw_t.begin_fill()

        if s == "Circle":
            draw_t.goto(cx, cy - VIS / 2)
            draw_t.pendown()
            draw_t.circle(VIS / 2)
            draw_t.penup()
            area = math.pi * (v1 ** 2)
            perimeter = 2 * math.pi * v1

        elif s == "Triangle":
            draw_t.goto(cx - VIS / 2, cy - VIS / 2)
            draw_t.pendown()
            draw_t.goto(cx + VIS / 2, cy - VIS / 2)  # Base
            draw_t.goto(cx, cy + VIS / 2)  # Apex
            draw_t.goto(cx - VIS / 2, cy - VIS / 2)  # Close
            draw_t.penup()
            area = 0.5 * v1 * v2
            hypot = math.sqrt((v1 / 2) ** 2 + v2 ** 2)
            perimeter = v1 + (2 * hypot)

        elif s in ["Rectangle", "Square"]:
            w_vis = VIS
            h_vis = VIS if s == "Square" else VIS * 0.6
            draw_t.goto(cx - w_vis / 2, cy - h_vis / 2)
            draw_t.pendown()
            for _ in range(2):
                draw_t.forward(w_vis)
                draw_t.left(90)
                draw_t.forward(h_vis)
                draw_t.left(90)
            draw_t.penup()
            act_w = v1
            act_h = v1 if s == "Square" else v2
            area = act_w * act_h
            perimeter = 2 * (act_w + act_h)

        elif s in ["Hexagon", "Polygon"]:
            sides = 6 if s == "Hexagon" else app_state["sides"]
            angle = 360 / sides
            side_vis = VIS * (2 * math.sin(math.pi / sides))
            draw_t.goto(cx - side_vis / 2, cy - VIS / 2)
            draw_t.pendown()
            for _ in range(sides):
                draw_t.forward(side_vis)
                draw_t.left(angle)
            draw_t.penup()
            area = (sides * v1 ** 2) / (4 * math.tan(math.pi / sides))
            perimeter = sides * v1

        elif s == "Parallelogram":
            slant_vis = VIS * 0.4
            h_vis = VIS * 0.6
            draw_t.goto(cx - VIS / 2, cy - h_vis / 2)
            draw_t.pendown()
            draw_t.forward(VIS)
            draw_t.goto(cx + VIS / 2 + slant_vis, cy + h_vis / 2)
            draw_t.backward(VIS)
            draw_t.goto(cx - VIS / 2, cy - h_vis / 2)
            draw_t.penup()
            real_slant_x = (slant_vis / VIS) * v1
            actual_slant = math.sqrt(v2 ** 2 + real_slant_x ** 2)
            area = v1 * v2
            perimeter = 2 * (v1 + actual_slant)

        draw_t.end_fill()
        # --- END DRAWING & FILL ---

        # --- MATH LABELS ---
        draw_t.color(THEME["text"])
        draw_t.goto(cx, -VIS / 2 - 80)
        draw_t.write(f"Area: {area:.2f} {u}²", align="center", font=("Courier", 18, "bold"))
        draw_t.goto(cx, -VIS / 2 - 110)
        draw_t.write(f"Perimeter: {perimeter:.2f} {u}", align="center", font=("Courier", 14, "bold"))

        if s == "Triangle":
            draw_t.goto(cx, -VIS / 2 - 140)
            draw_t.write(f"Hypotenuse: {hypot:.2f} {u}", align="center", font=("Courier", 12, "italic"))


    def render_3d(s, v1, v2, u, cx, cy, VIS):
        draw_t.clear()
        draw_t.pensize(2)

        # --- DYNAMIC COLORS ---
        # Pull the custom color from app_state; default to Cyan if not set
        FILL_COLOR = app_state.get("color", "#00FFFF")

        # Logic to make the edges slightly darker than the fill color
        # If using standard CAD colors, we can keep the Dark Cyan or set it to Black
        EDGE_COLOR = "#008B8B"  # Dark Cyan for crisp lines

        vol = 0

        if s == "Cylinder":
            # Helper for drawing a filled ellipse cap
            def oval_cap(y):
                draw_t.penup()
                draw_t.goto(cx + VIS / 2, cy + y)
                draw_t.pendown()
                draw_t.begin_fill()
                for i in range(361):
                    r = math.radians(i)
                    draw_t.goto(cx + (VIS / 2) * math.cos(r), (cy + y) + (VIS / 6) * math.sin(r))
                draw_t.end_fill()

            # 1. Fill the Rectangular Body FIRST
            draw_t.color(FILL_COLOR)
            draw_t.penup()
            draw_t.goto(cx - VIS / 2, cy - VIS / 2)
            draw_t.begin_fill()
            draw_t.goto(cx + VIS / 2, cy - VIS / 2)
            draw_t.goto(cx + VIS / 2, cy + VIS / 2)
            draw_t.goto(cx - VIS / 2, cy + VIS / 2)
            draw_t.goto(cx - VIS / 2, cy - VIS / 2)
            draw_t.end_fill()

            # 2. Fill the Top and Bottom Caps
            oval_cap(-VIS / 2)  # Bottom
            oval_cap(VIS / 2)  # Top

            # 3. Draw Dark Outlines (After all fills are done)
            draw_t.color(EDGE_COLOR)
            # Vertical side lines
            for dx in [-VIS / 2, VIS / 2]:
                draw_t.penup()
                draw_t.goto(cx + dx, cy - VIS / 2)
                draw_t.pendown()
                draw_t.goto(cx + dx, cy + VIS / 2)

            # Ellipse outlines (No fill)
            for y in [-VIS / 2, VIS / 2]:
                draw_t.penup()
                draw_t.goto(cx + VIS / 2, cy + y)
                draw_t.pendown()
                for i in range(361):
                    r = math.radians(i)
                    draw_t.goto(cx + (VIS / 2) * math.cos(r), (cy + y) + (VIS / 6) * math.sin(r))

            vol = math.pi * (v1 ** 2) * v2


        elif s in ["Cube", "Cuboid"]:
            w_vis = VIS
            h_vis = VIS if s == "Cube" else VIS * 0.6
            off = 60
            f_x, f_y = cx - w_vis / 2, cy - h_vis / 2
            b_x, b_y = f_x + off, f_y + off

            # 1. Fill all faces bright Cyan
            draw_t.color(FILL_COLOR)
            for start_x, start_y in [(b_x, b_y), (f_x, f_y)]:  # Back then Front
                draw_t.penup()
                draw_t.goto(start_x, start_y)
                draw_t.begin_fill()
                for _ in range(2): draw_t.forward(w_vis); draw_t.left(90); draw_t.forward(h_vis); draw_t.left(90)
                draw_t.end_fill()
            draw_t.begin_fill()  # Connecting walls
            draw_t.goto(f_x, f_y + h_vis)
            draw_t.goto(b_x, b_y + h_vis)
            draw_t.goto(b_x + w_vis, b_y + h_vis)
            draw_t.goto(f_x + w_vis, f_y + h_vis)
            draw_t.goto(f_x + w_vis, f_y)
            draw_t.goto(b_x + w_vis, b_y)
            draw_t.goto(b_x + w_vis, b_y + h_vis)
            draw_t.goto(f_x + w_vis, f_y + h_vis)
            draw_t.end_fill()

            # 2. Draw Dark Cyan Outlines
            draw_t.color(EDGE_COLOR)
            for start_x, start_y in [(f_x, f_y), (b_x, b_y)]:
                draw_t.penup()
                draw_t.goto(start_x, start_y)
                draw_t.pendown()
                for _ in range(2): draw_t.forward(w_vis); draw_t.left(90); draw_t.forward(h_vis); draw_t.left(90)
            for dx, dy in [(0, 0), (w_vis, 0), (w_vis, h_vis), (0, h_vis)]:
                draw_t.penup()
                draw_t.goto(f_x + dx, f_y + dy)
                draw_t.pendown()
                draw_t.goto(b_x + dx, b_y + dy)
            vol = v1 ** 3 if s == "Cube" else v1 * v2 * app_state.get("depth", 10)


        elif s == "Pyramid":

            off = 60

            apex = (cx, cy + VIS / 2)

            # Corners: BL, BR, TR, TL

            c = [(cx - VIS / 2, cy - VIS / 2), (cx + VIS / 2, cy - VIS / 2),

                 (cx + VIS / 2 + off, cy - VIS / 2 + off), (cx - VIS / 2 + off, cy - VIS / 2 + off)]

            # 1. Fill the Base FIRST

            draw_t.color(FILL_COLOR)

            draw_t.penup()

            draw_t.goto(c[0])

            draw_t.pendown()

            draw_t.begin_fill()

            for p in c: draw_t.goto(p)

            draw_t.goto(c[0])

            draw_t.end_fill()

            # 2. Fill each Face SEPARATELY (This fixes the ghost triangle)

            for i in range(4):
                draw_t.penup()

                draw_t.goto(c[i])  # Start at a corner

                draw_t.pendown()

                draw_t.begin_fill()

                draw_t.goto(apex)  # Go to top

                draw_t.goto(c[(i + 1) % 4])  # Go to next corner

                draw_t.goto(c[i])  # Close the triangle

                draw_t.end_fill()

            # 3. Draw Dark Outlines

            draw_t.color(EDGE_COLOR)

            # Base outline

            draw_t.penup()
            draw_t.goto(c[0])
            draw_t.pendown()

            for p in c: draw_t.goto(p)

            draw_t.goto(c[0])

            # Apex lines

            for p in c:
                draw_t.penup()

                draw_t.goto(p)

                draw_t.pendown()

                draw_t.goto(apex)

            vol = (1 / 3) * (v1 ** 2) * v2


        elif s == "Sphere":
            # 1. Solid Fill
            draw_t.penup()
            draw_t.goto(cx, cy - VIS / 2)
            draw_t.color(FILL_COLOR)
            draw_t.begin_fill()
            draw_t.circle(VIS / 2)
            draw_t.end_fill()
            # 2. Outlines (Outer ring and Depth belt)
            draw_t.color(EDGE_COLOR)
            draw_t.pendown()
            draw_t.circle(VIS / 2)
            draw_t.penup()
            draw_t.goto(cx + VIS / 2, cy)
            draw_t.pendown()
            for i in range(361):
                r = math.radians(i)
                draw_t.goto(cx + (VIS / 2) * math.cos(r), cy + (VIS / 6) * math.sin(r))
            vol = (4 / 3) * math.pi * (v1 ** 3)

        # Label
        draw_t.penup()
        draw_t.color(THEME["text"])
        draw_t.goto(cx, -VIS / 2 - 120)
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

        shapes = ["Triangle", "Circle", "Rectangle", "Square", "Hexagon", "Parallelogram", "Polygon"] if app_state["category"] == "2D" \
            else ["Cube", "Cuboid", "Cylinder", "Pyramid", "Sphere"]
        y = 280
        for s in shapes:
            draw_ui_button(s, -680, y, 260, 35, app_state["shape"] == s)
            y -= 45

        # --- BUTTONS AT THE BOTTOM ---
        draw_ui_button("CHANGE COLOR", -680, -230, 260, 45, False)
        draw_ui_button("EXPORT DATA", -680, -290, 260, 45, False)
        draw_ui_button("EDIT DIMENSIONS", -680, -350, 260, 45, False)
        draw_ui_button("EXIT", -680, -410, 260, 45, False)


    def refresh():
        draw_sidebar()
        draw_t.clear()
        cx, cy, VIS = 200, 0, 300

        # Ensure draw_t is using the latest app_state color
        draw_t.color(app_state.get("color", THEME["text"]))

        draw_specs(cx, cy, VIS)

        if app_state["category"] == "2D":
            # Pass the color or let render_2d pull it from app_state
            render_2d(app_state["shape"], app_state["val1"], app_state["val2"], app_state["unit"], cx, cy, VIS)
        else:
            render_3d(app_state["shape"], app_state["val1"], app_state["val2"], app_state["unit"], cx, cy, VIS)

        screen.update()


    def save_results():
        try:
            sh = app_state["shape"]
            u = app_state["unit"]
            v1, v2 = app_state["val1"], app_state["val2"]

            filename = f"CAD_Export_{sh}.txt"
            with open(filename, "w") as f:
                f.write(f"--- Designer Pro CAD Export ---\n")
                f.write(f"Shape: {sh}\n")
                f.write(f"Dimensions: {v1}{u} x {v2}{u}\n")

                if app_state["category"] == "2D":
                    # Note: You can pull these logic blocks from your render_2d function
                    area = v1 * v2  # Simplified example
                    f.write(f"Area: {area:.2f} {u}2\n")
                else:
                    vol = math.pi * (v1 ** 2) * v2 if sh == "Cylinder" else v1 ** 3
                    f.write(f"Volume: {vol:.2f} {u}3\n")

                f.write(f"-------------------------------\n")

            # UI Feedback
            screen.textinput("Success", f"Data saved to {filename}\nPress OK to continue.")
        except Exception as e:
            screen.textinput("Error", f"Failed to save: {e}")


    def handle_click(x, y):
        # --- Category Selection (2D vs 3D) ---
        if -680 < x < -555 and 340 < y < 380:
            app_state["category"] = "2D"
            app_state["shape"] = "Rectangle"
            app_state["color"] = "#2ECC71"  # Green default for 2D
        elif -545 < x < -420 and 340 < y < 380:
            app_state["category"] = "3D"
            app_state["shape"] = "Cube"
            app_state["color"] = "#00FFFF"  # Cyan default for 3D

        # --- Sidebar Button Logic ---
        elif -680 < x < -420:
            # Determine available shapes
            if app_state["category"] == "2D":
                shapes = ["Triangle", "Circle", "Rectangle", "Square", "Hexagon", "Parallelogram", "Polygon"]
            else:
                shapes = ["Cube", "Cuboid", "Cylinder", "Pyramid", "Sphere"]

            # 1. Shape Selection
            y_btn = 280
            for s in shapes:
                if y_btn < y < y_btn + 35:
                    app_state["shape"] = s
                y_btn -= 45

            # 2. CHANGE COLOR Button (-230 range)
            if -230 < y < -185:
                new_col = screen.textinput("Color Picker", "Enter color (Name or Hex):")
                if new_col:
                    try:
                        ui_t.color(new_col)  # Test validity
                        app_state["color"] = new_col
                    except:
                        pass

            # 3. EXPORT DATA Button (-290 range)
            elif -290 < y < -245:
                save_results()

            # 4. EDIT DIMENSIONS Button (-350 range)
            elif -350 < y < -305:
                sh = app_state["shape"]
                u = app_state["unit"]

                if sh == "Cuboid":
                    w = screen.numinput("Cuboid", f"Enter Width ({u}):", default=app_state["val1"])
                    h = screen.numinput("Cuboid", f"Enter Height ({u}):", default=app_state["val2"])
                    d = screen.numinput("Cuboid", f"Enter Depth ({u}):", default=app_state.get("depth", 10.0))
                    if w: app_state["val1"] = w
                    if h: app_state["val2"] = h
                    if d: app_state["depth"] = d

                elif sh == "Cylinder":
                    r = screen.numinput("Cylinder", f"Enter Radius ({u}):", default=app_state["val1"])
                    h = screen.numinput("Cylinder", f"Enter Height ({u}):", default=app_state["val2"])
                    if r: app_state["val1"] = r
                    if h: app_state["val2"] = h

                elif sh in ["Circle", "Sphere"]:
                    v = screen.numinput(sh, f"Enter Radius ({u}):", default=app_state["val1"])
                    if v: app_state["val1"] = v

                elif sh in ["Square", "Cube"]:
                    v = screen.numinput(sh, f"Enter Side Length ({u}):", default=app_state["val1"])
                    if v: app_state["val1"] = v

                elif sh == "Polygon":
                    v1 = screen.numinput("Polygon", f"Enter Side Length ({u}):", default=app_state["val1"])
                    v2 = screen.numinput("Polygon", "Enter Number of Sides:", default=app_state["sides"])
                    if v1: app_state["val1"] = v1
                    if v2: app_state["sides"] = int(v2)

                else:  # Triangle, Rectangle, Parallelogram, Pyramid
                    v1 = screen.numinput(sh, f"Enter Base/Width ({u}):", default=app_state["val1"])
                    v2 = screen.numinput(sh, f"Enter Height ({u}):", default=app_state["val2"])
                    if v1: app_state["val1"] = v1
                    if v2: app_state["val2"] = v2

            # 5. EXIT Button (-410 range)
            elif -410 < y < -365:
                screen.bye()
                return

        refresh()


    draw_grid()
    refresh()
    screen.onclick(handle_click)
    screen.listen()
    turtle.done()
