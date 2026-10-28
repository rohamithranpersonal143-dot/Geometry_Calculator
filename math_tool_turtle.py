if __name__ == '__main__':
    import math
    import turtle
    import time
    import tkinter as tk

    # --- INITIALIZATION ---
    screen = turtle.Screen()
    screen.bgcolor("#0B0E14")
    screen.title("Blueprint Visualizer Pro")
    screen.tracer(0)

    mode = screen.textinput("Screen Mode", "F for Fullscreen / W for Windowed:")
    if mode and mode.strip().upper() == 'F':
        screen.setup(width=1.0, height=1.0)
        screen.getcanvas().winfo_toplevel().attributes("-fullscreen", True)
    else:
        screen.setup(width=1000, height=800)

    W_WIDTH, W_HEIGHT = screen.window_width(), screen.window_height()
    t = turtle.Turtle()
    t.pensize(2)
    t.hideturtle()
    gt = turtle.Turtle()
    gt.hideturtle()
    gt.color("#1E2530")
    SHAPE_COLOR = "#E0FFFF"


    def draw_grid():
        gt.clear()
        for x in range(int(-W_WIDTH / 2), int(W_WIDTH / 2), 50):
            gt.penup()
            gt.goto(x, -W_HEIGHT / 2)
            gt.pendown()
            gt.goto(x, W_HEIGHT / 2)
        for y in range(int(-W_HEIGHT / 2), int(W_HEIGHT / 2), 50):
            gt.penup()
            gt.goto(-W_WIDTH / 2, y)
            gt.pendown()
            gt.goto(W_WIDTH / 2, y)


    draw_grid()
    screen.update()
    screen.tracer(1)
    t.speed(3)

    while True:
        try:
            screen.update()
            # Ask for unit  at the start of each loop
            unit = screen.textinput("Units", "Enter measurement unit (cm, m, in, ft):")
            if unit is None: unit = "units"

            cat_input = screen.textinput("Blueprint Category", "Choose: 2D or 3D (or 'Exit')")
            if cat_input is None or cat_input.strip().lower() == 'exit': break

            category = cat_input.strip().upper()
            cx, cy = 0, 0
            VIS_SIZE = W_WIDTH / 4
            VIS_OFF = VIS_SIZE * 0.3
            # Clear the previous shape and all its measurements
            t.clear()
            t.penup()
            t.home()
            t.setheading(0)
            t.color(SHAPE_COLOR)
            t.pensize(2)
            if category == "3D":
                shape_input = screen.textinput(
                    "3D Visualizer",
                    "Cube, Cylinder, Pyramid, Sphere, Cone, "
                    "Triangular Prism, Rectangular Prism"
                )

                if shape_input is None:
                    continue

                shape = " ".join(shape_input.strip().lower().split())

                if shape == "cube":
                    real_s = screen.numinput("Cube", f"Side Length ({unit}):", default=10)
                    if real_s:
                        def draw_box(x, y, c):
                            t.penup()
                            t.goto(x, y)
                            t.pendown()
                            t.color(c)
                            for _ in range(4): t.forward(VIS_SIZE); t.left(90)


                        draw_box(cx - VIS_SIZE / 2 + VIS_OFF, cy - VIS_SIZE / 2 + VIS_OFF, "#4A6670")
                        for x, y in [(cx - VIS_SIZE / 2, cy - VIS_SIZE / 2), (cx + VIS_SIZE / 2, cy - VIS_SIZE / 2),
                                     (cx + VIS_SIZE / 2, cy + VIS_SIZE / 2), (cx - VIS_SIZE / 2, cy + VIS_SIZE / 2)]:
                            t.penup()
                            t.goto(x, y)
                            t.pendown()
                            t.goto(x + VIS_OFF, y + VIS_OFF)
                        draw_box(cx - VIS_SIZE / 2, cy - VIS_SIZE / 2, SHAPE_COLOR)
                        t.penup()
                        t.goto(cx, cy - VIS_SIZE / 2 - 25)
                        t.write(f"L: {real_s} {unit}", align="center", font=("Courier", 10, "bold"))
                        t.goto(cx + VIS_SIZE / 2 + 10, cy)
                        t.write(f"H: {real_s} {unit}", align="left", font=("Courier", 10, "bold"))
                        t.goto(cx + VIS_SIZE / 2 + VIS_OFF / 2 + 10, cy - VIS_SIZE / 2 + VIS_OFF / 2)
                        t.write(f"W: {real_s} {unit}", align="left", font=("Courier", 10, "bold"))
                        t.goto(0, -VIS_SIZE / 2 - 65)
                        t.write(f"Volume: {real_s ** 3:.2f} {unit}³", align="center", font=("Courier", 14, "bold"))

                elif shape == "pyramid":
                    real_s = screen.numinput("Pyramid", f"Base Side ({unit}):", default=10)
                    real_h = screen.numinput("Pyramid", f"Height ({unit}):", default=10)
                    if real_s and real_h:
                        base_y = cy - VIS_SIZE / 2
                        t.color("#4A6670")
                        pts = [(cx - VIS_SIZE / 2, base_y), (cx + VIS_SIZE / 2, base_y),
                               (cx + VIS_SIZE / 2 + VIS_OFF, base_y + VIS_OFF),
                               (cx - VIS_SIZE / 2 + VIS_OFF, base_y + VIS_OFF)]
                        t.penup()
                        t.goto(pts[0])
                        t.pendown()
                        for p in pts[1:]: t.goto(p)
                        t.goto(pts[0])
                        t.color(SHAPE_COLOR)
                        apex = (cx + VIS_OFF / 2, base_y + VIS_SIZE)
                        for p in pts: t.penup(); t.goto(p); t.pendown(); t.goto(apex)
                        t.penup()
                        t.goto(cx + VIS_SIZE / 2 + VIS_OFF + 20, cy)
                        t.write(f"H: {real_h} {unit}", align="left", font=("Courier", 10, "bold"))
                        t.goto(cx, base_y - 25)
                        t.write(f"B: {real_s} {unit}", align="center", font=("Courier", 10, "bold"))
                        t.goto(0, base_y - 65)
                        t.write(f"Volume: {(1 / 3) * (real_s ** 2) * real_h:.2f} {unit}³", align="center",
                                font=("Courier", 14, "bold"))

                elif shape == "cylinder":
                    real_r = screen.numinput("Cylinder", f"Radius ({unit}):", default=5)
                    real_h = screen.numinput("Cylinder", f"Height ({unit}):", default=10)
                    if real_r and real_h:
                        tilt = 0.4


                        def draw_oval(x, y, color):
                            t.penup()
                            t.goto(x + VIS_SIZE / 2, y)
                            t.pendown()
                            t.color(color)
                            for i in range(361):
                                rad = math.radians(i)
                                t.goto(x + (VIS_SIZE / 2) * math.cos(rad), y + (VIS_SIZE / 2 * tilt) * math.sin(rad))


                        draw_oval(cx, cy - VIS_SIZE / 2, "#4A6670")
                        draw_oval(cx, cy + VIS_SIZE / 2, SHAPE_COLOR)
                        for sx in [-VIS_SIZE / 2, VIS_SIZE / 2]:
                            t.penup()
                            t.goto(cx + sx, cy - VIS_SIZE / 2)
                            t.pendown()
                            t.goto(cx + sx, cy + VIS_SIZE / 2)
                        t.penup()
                        t.goto(cx + VIS_SIZE / 2 + 10, cy)
                        t.write(f"H: {real_h} {unit}", align="left", font=("Courier", 10, "bold"))
                        t.goto(cx, cy + VIS_SIZE / 2 + (VIS_SIZE / 2 * tilt) + 5)
                        t.write(f"R: {real_r} {unit}", align="center", font=("Courier", 10, "bold"))
                        t.goto(0, -VIS_SIZE / 2 - 65)
                        t.write(f"Volume: {math.pi * (real_r ** 2) * real_h:.2f} {unit}³", align="center",
                                font=("Courier", 14, "bold"))

                elif shape == "sphere":
                    real_r = screen.numinput(
                        "Sphere",
                        f"Radius ({unit}):",
                        default=5,
                        minval=0.001
                    )

                    if real_r is not None and real_r > 0:
                        # Blueprint sphere dimensions
                        draw_r = min(W_WIDTH / 5, W_HEIGHT / 4)

                        # Draw the outer circle
                        t.color(SHAPE_COLOR)
                        t.pensize(2)
                        t.penup()
                        t.goto(cx, cy - draw_r)
                        t.pendown()
                        t.circle(draw_r)
                        t.penup()

                        # Draw horizontal elliptical latitude lines
                        for fraction in [-0.75, -0.4, 0, 0.4, 0.75]:
                            y = cy + fraction * draw_r
                            oval_r = draw_r * math.sqrt(
                                1 - fraction**2
                            )

                            t.penup()
                            t.goto(cx - oval_r, y)
                            t.pendown()

                            for i in range(61):
                                angle = math.radians(i * 6)
                                t.goto(
                                    cx + oval_r * math.cos(angle),
                                    y + oval_r * 0.18 * math.sin(angle)
                                )

                            t.penup()

                        # Draw vertical meridian ellipses
                        for factor in [0.4, 0.75]:
                            for sign in [-1, 1]:
                                t.penup()
                                t.goto(cx, cy - draw_r)
                                t.pendown()

                                for i in range(61):
                                    angle = math.radians(i * 6)
                                    t.goto(
                                        cx + sign * draw_r * factor
                                        * math.sin(angle),
                                        cy + draw_r * math.cos(angle)
                                    )

                                t.penup()

                        # Radius indicator
                        t.color("#4A6670")
                        t.goto(cx, cy)
                        t.pendown()
                        t.goto(cx + draw_r, cy)
                        t.penup()

                        t.color(SHAPE_COLOR)

                        # Measurements
                        surface_area = 4 * math.pi * real_r**2
                        volume = (4 / 3) * math.pi * real_r**3

                        t.goto(cx, cy - draw_r - 30)
                        t.write(
                            f"Radius: {real_r} {unit}",
                            align="center",
                            font=("Courier", 10, "bold")
                        )

                        t.goto(cx, cy - draw_r - 55)
                        t.write(
                            f"Surface Area: {surface_area:.2f} {unit}²",
                            align="center",
                            font=("Courier", 11, "bold")
                        )

                        t.goto(cx, cy - draw_r - 85)
                        t.write(
                            f"Volume: {volume:.2f} {unit}³",
                            align="center",
                            font=("Courier", 14, "bold")
                        )
                elif shape == "cone":
                    real_r = screen.numinput(
                        "Cone",
                        f"Base radius ({unit}):",
                        default=5,
                        minval=0.001
                    )

                    if real_r is not None and real_r > 0:
                        real_h = screen.numinput(
                            "Cone",
                            f"Height ({unit}):",
                            default=10,
                            minval=0.001
                        )

                        if real_h is not None and real_h > 0:
                            # Blueprint drawing dimensions
                            draw_r = min(W_WIDTH / 6, W_HEIGHT / 5)
                            draw_h = draw_r * 1.8

                            # Draw elliptical base
                            t.color(SHAPE_COLOR)
                            t.pensize(2)
                            t.penup()
                            t.goto(cx - draw_r, cy - draw_h / 2)
                            t.pendown()

                            for i in range(61):
                                angle = math.radians(i * 6)
                                t.goto(
                                    cx + draw_r * math.cos(angle),
                                    cy - draw_h / 2
                                    + draw_r * 0.3 * math.sin(angle)
                                )

                            t.penup()

                            # Draw cone apex
                            apex_x = cx
                            apex_y = cy + draw_h / 2

                            # Draw sides
                            t.goto(apex_x, apex_y)
                            t.pendown()
                            t.goto(cx - draw_r, cy - draw_h / 2)
                            t.penup()

                            t.goto(apex_x, apex_y)
                            t.pendown()
                            t.goto(cx + draw_r, cy - draw_h / 2)
                            t.penup()

                            # Dashed rear edge of base
                            t.color("#4A6670")
                            t.goto(cx - draw_r, cy - draw_h / 2)
                            t.setheading(0)

                            for i in range(30):
                                t.pendown() if i % 2 == 0 else t.penup()
                                t.forward((2 * draw_r) / 30)

                            t.penup()
                            t.color(SHAPE_COLOR)

                            # Measurements
                            surface_area = (
                                math.pi * real_r
                                * (real_r + math.sqrt(real_r**2 + real_h**2))
                            )
                            volume = (
                                math.pi * real_r**2 * real_h / 3
                            )

                            t.goto(cx, cy - draw_h / 2 - 35)
                            t.write(
                                f"Radius: {real_r} {unit} | Height: {real_h} {unit}",
                                align="center",
                                font=("Courier", 10, "bold")
                            )

                            t.goto(cx, cy - draw_h / 2 - 60)
                            t.write(
                                f"Surface Area: {surface_area:.2f} {unit}²",
                                align="center",
                                font=("Courier", 11, "bold")
                            )

                            t.goto(cx, cy - draw_h / 2 - 90)
                            t.write(
                                f"Volume: {volume:.2f} {unit}³",
                                align="center",
                                font=("Courier", 14, "bold")
                            )
                elif shape == "triangular prism":
                    base = screen.numinput(
                        "Triangular Prism",
                        f"Triangle base ({unit}):",
                        default=6,
                        minval=0.001
                    )

                    if base is not None and base > 0:
                        tri_h = screen.numinput(
                            "Triangular Prism",
                            f"Triangle height ({unit}):",
                            default=4,
                            minval=0.001
                        )

                        if tri_h is not None and tri_h > 0:
                            length = screen.numinput(
                                "Triangular Prism",
                                f"Prism length ({unit}):",
                                default=8,
                                minval=0.001
                            )

                            if length is not None and length > 0:
                                # Blueprint drawing dimensions
                                scale = min(
                                    W_WIDTH / 12,
                                    W_HEIGHT / 10
                                )
                                draw_b = base * scale
                                draw_h = tri_h * scale
                                draw_l = length * scale * 0.6

                                # Keep the drawing within the screen
                                max_draw = min(
                                    W_WIDTH * 0.35,
                                    W_HEIGHT * 0.3
                                )
                                factor = min(
                                    1,
                                    max_draw / max(
                                        draw_b, draw_h, draw_l
                                    )
                                )

                                draw_b *= factor
                                draw_h *= factor
                                draw_l *= factor

                                # Front triangle
                                left = (cx - draw_b / 2, cy - draw_h / 2)
                                right = (cx + draw_b / 2, cy - draw_h / 2)
                                top = (cx, cy + draw_h / 2)

                                # Back triangle, offset for perspective
                                offset_x = draw_l * 0.6
                                offset_y = draw_l * 0.4

                                back_left = (
                                    left[0] + offset_x,
                                    left[1] + offset_y
                                )
                                back_right = (
                                    right[0] + offset_x,
                                    right[1] + offset_y
                                )
                                back_top = (
                                    top[0] + offset_x,
                                    top[1] + offset_y
                                )

                                t.color(SHAPE_COLOR)
                                t.pensize(2)

                                # Draw front triangle
                                t.penup()
                                t.goto(left)
                                t.pendown()
                                t.goto(right)
                                t.goto(top)
                                t.goto(left)
                                t.penup()

                                # Draw back triangle
                                t.goto(back_left)
                                t.pendown()
                                t.goto(back_right)
                                t.goto(back_top)
                                t.goto(back_left)
                                t.penup()

                                # Connect corresponding vertices
                                for front, back in [
                                    (left, back_left),
                                    (right, back_right),
                                    (top, back_top)
                                ]:
                                    t.goto(front)
                                    t.pendown()
                                    t.goto(back)
                                    t.penup()

                                # Measurements
                                triangle_area = base * tri_h / 2
                                volume = triangle_area * length

                                # Surface area needs the third triangle side.
                                # Assume an isosceles triangle for this formula.
                                slant = math.sqrt(
                                    (base / 2) ** 2 + tri_h ** 2
                                )
                                surface_area = (
                                    base * length
                                    + 2 * slant * length
                                    + base * tri_h
                                )

                                t.color(SHAPE_COLOR)
                                t.goto(cx, cy - draw_h / 2 - draw_l * 0.4 - 35)
                                t.write(
                                    f"Base: {base} {unit} | "
                                    f"Triangle height: {tri_h} {unit}",
                                    align="center",
                                    font=("Courier", 10, "bold")
                                )

                                t.goto(cx, cy - draw_h / 2 - draw_l * 0.4 - 60)
                                t.write(
                                    f"Length: {length} {unit} | "
                                    f"Surface Area: {surface_area:.2f} {unit}²",
                                    align="center",
                                    font=("Courier", 10, "bold")
                                )

                                t.goto(cx, cy - draw_h / 2 - draw_l * 0.4 - 85)
                                t.write(
                                    f"Volume: {volume:.2f} {unit}³",
                                    align="center",
                                    font=("Courier", 13, "bold")
                                )
                elif shape == "rectangular prism":
                    real_l = screen.numinput(
                        "Rectangular Prism",
                        f"Length ({unit}):",
                        default=8,
                        minval=0.001
                    )

                    if real_l is not None and real_l > 0:
                        real_w = screen.numinput(
                            "Rectangular Prism",
                            f"Width ({unit}):",
                            default=5,
                            minval=0.001
                        )

                        if real_w is not None and real_w > 0:
                            real_h = screen.numinput(
                                "Rectangular Prism",
                                f"Height ({unit}):",
                                default=4,
                                minval=0.001
                            )

                            if real_h is not None and real_h > 0:
                                # Blueprint drawing dimensions
                                scale = min(
                                    W_WIDTH / 12,
                                    W_HEIGHT / 10
                                )

                                draw_l = real_l * scale
                                draw_w = real_w * scale * 0.6
                                draw_h = real_h * scale

                                # Scale down if the prism is too large
                                max_draw = min(
                                    W_WIDTH * 0.35,
                                    W_HEIGHT * 0.3
                                )
                                factor = min(
                                    1,
                                    max_draw / max(
                                        draw_l, draw_w, draw_h
                                    )
                                )

                                draw_l *= factor
                                draw_w *= factor
                                draw_h *= factor

                                # Front rectangle
                                left = (cx - draw_l / 2, cy - draw_h / 2)
                                right = (cx + draw_l / 2, cy - draw_h / 2)
                                top_right = (
                                    cx + draw_l / 2,
                                    cy + draw_h / 2
                                )
                                top_left = (
                                    cx - draw_l / 2,
                                    cy + draw_h / 2
                                )

                                # Back rectangle offset for perspective
                                ox = draw_w * 0.7
                                oy = draw_w * 0.5

                                back_left = (left[0] + ox, left[1] + oy)
                                back_right = (right[0] + ox, right[1] + oy)
                                back_top_right = (
                                    top_right[0] + ox,
                                    top_right[1] + oy
                                )
                                back_top_left = (
                                    top_left[0] + ox,
                                    top_left[1] + oy
                                )

                                t.color(SHAPE_COLOR)
                                t.pensize(2)

                                # Draw front face
                                t.penup()
                                t.goto(left)
                                t.pendown()
                                t.goto(right)
                                t.goto(top_right)
                                t.goto(top_left)
                                t.goto(left)
                                t.penup()

                                # Draw back face
                                t.goto(back_left)
                                t.pendown()
                                t.goto(back_right)
                                t.goto(back_top_right)
                                t.goto(back_top_left)
                                t.goto(back_left)
                                t.penup()

                                # Connect front and back corners
                                for front, back in [
                                    (left, back_left),
                                    (right, back_right),
                                    (top_right, back_top_right),
                                    (top_left, back_top_left)
                                ]:
                                    t.goto(front)
                                    t.pendown()
                                    t.goto(back)
                                    t.penup()

                                # Calculations
                                surface_area = 2 * (
                                    real_l * real_w
                                    + real_l * real_h
                                    + real_w * real_h
                                )
                                volume = real_l * real_w * real_h

                                # Display measurements
                                label_y = (
                                    cy - draw_h / 2 - draw_w * 0.5 - 35
                                )

                                t.color(SHAPE_COLOR)
                                t.goto(cx, label_y)
                                t.write(
                                    f"L: {real_l} {unit} | "
                                    f"W: {real_w} {unit} | "
                                    f"H: {real_h} {unit}",
                                    align="center",
                                    font=("Courier", 10, "bold")
                                )

                                t.goto(cx, label_y - 25)
                                t.write(
                                    f"Surface Area: {surface_area:.2f} {unit}²",
                                    align="center",
                                    font=("Courier", 11, "bold")
                                )

                                t.goto(cx, label_y - 55)
                                t.write(
                                    f"Volume: {volume:.2f} {unit}³",
                                    align="center",
                                    font=("Courier", 14, "bold")
                                )

            elif category == "2D":
                shape_input = screen.textinput("2D Designer",
                                               "Triangle, Circle, Rectangle, Square, Hexagon, Parallelogram , Custom Polygon",)
                if not shape_input: continue
                shape = shape_input.strip().capitalize()
                t.clear()
                t.color(SHAPE_COLOR)

                if shape == "Triangle":
                    b_v = screen.numinput("Triangle", f"Base ({unit}):", default=10)
                    h_v = screen.numinput("Triangle", f"Height ({unit}):", default=10)
                    if b_v and h_v:
                        sc = (W_WIDTH / 4) / max(b_v, h_v)
                        b, h = b_v * sc, h_v * sc
                        hyp = math.sqrt(b_v ** 2 + h_v ** 2)
                        ang_b = math.degrees(math.atan2(h_v, b_v))
                        ang_t = 90 - ang_b
                        t.penup()
                        t.goto(cx - b / 2, cy - h / 2)
                        t.pendown()
                        t.goto(cx + b / 2, cy - h / 2)
                        t.write(" 90°", font=("Courier", 10, "bold"))
                        t.goto(cx + b / 2, cy + h / 2)
                        t.write(f" {ang_t:.1f}°", font=("Courier", 10, "bold"))
                        t.goto(cx - b / 2, cy - h / 2)
                        t.write(f" {ang_b:.1f}°", font=("Courier", 10, "bold"))
                        t.penup()
                        t.goto(cx, cy - h / 2 - 30)
                        t.write(f"B: {b_v} {unit}", align="center", font=("Courier", 10, "bold"))
                        t.goto(cx + b / 2 + 10, cy)
                        t.write(f"H: {h_v} {unit}", align="left", font=("Courier", 10, "bold"))
                        t.goto(cx, cy + h / 2 + 15)
                        t.write(f"Hyp: {hyp:.2f} {unit}", align="center", font=("Courier", 10, "bold"))
                        t.goto(0, -h / 2 - 60)
                        t.write(f"Area: {0.5 * b_v * h_v:.2f} {unit}²", align="center", font=("Courier", 14, "bold"))

                elif shape in ["Rectangle", "Square"]:
                    l_v = screen.numinput(shape, f"Length ({unit}):", default=10)
                    w_v = l_v if shape == "Square" else screen.numinput(shape, f"Width ({unit}):", default=5)
                    if l_v and w_v:
                        sc = (W_WIDTH / 4) / max(l_v, w_v)
                        l, w = l_v * sc, w_v * sc
                        t.penup()
                        t.goto(cx - l / 2, cy - w / 2)
                        t.pendown()
                        for _ in range(2):
                            t.forward(l)
                            t.write(" 90°", font=("Courier", 10, "bold"))
                            t.left(90)
                            t.forward(w)
                            t.write(" 90°", font=("Courier", 10, "bold"))
                            t.left(90)
                        t.penup()
                        t.goto(cx, cy - w / 2 - 30)
                        t.write(f"L: {l_v} {unit}", align="center", font=("Courier", 10, "bold"))
                        t.goto(cx + l / 2 + 10, cy)
                        t.write(f"W: {w_v} {unit}", align="left", font=("Courier", 10, "bold"))
                        t.goto(0, -w / 2 - 60)
                        t.write(f"Area: {l_v * w_v:.2f} {unit}²", align="center", font=("Courier", 14, "bold"))




                elif shape == "Hexagon":
                    s_v = screen.numinput("Hexagon", f"Side ({unit}):", default=10)
                    if s_v:
                        sc = (W_HEIGHT / 6) / s_v
                        s = s_v * sc
                        t.penup()
                        t.goto(-s / 2, -s)
                        t.pendown()
                        for _ in range(6): t.forward(s); t.write(" 120°", font=("Courier", 10, "bold")); t.left(60)
                        t.penup()
                        t.goto(0, -s - 30)
                        t.write(f"S: {s_v} {unit}", align="center", font=("Courier", 10, "bold"))
                        t.goto(0, -s - 60)
                        t.write(f"Area: {(3 * math.sqrt(3) / 2) * (s_v ** 2):.2f} {unit}²", align="center",
                                font=("Courier", 14, "bold"))

                elif shape == "Parallelogram":
                    b_v = screen.numinput("Para", f"Base ({unit}):")
                    h_v = screen.numinput("Para", f"Height ({unit}):")
                    s_v = screen.numinput("Para", f"Slant ({unit}):")
                    if b_v and h_v and s_v:
                        sc = (W_WIDTH / 4) / max(b_v, h_v, s_v)
                        b, h, slant = b_v * sc, h_v * sc, s_v * sc
                        ang = math.degrees(math.asin(min(1, h_v / s_v)))
                        t.penup()
                        t.goto(-b / 2, -h / 2)
                        t.pendown()
                        for _ in range(2):
                            t.forward(b)
                            t.write(f" {ang:.1f}°", font=("Courier", 10, "bold"))
                            t.left(ang)
                            t.forward(slant)
                            t.write(f" {180 - ang:.1f}°", font=("Courier", 10, "bold"))
                            t.left(180 - ang)
                        t.penup()
                        t.goto(cx, cy - h / 2 - 30)
                        t.write(f"B: {b_v} {unit}", align="center", font=("Courier", 10, "bold"))
                        t.goto(cx + b / 2 + 10, cy)
                        t.write(f"H: {h_v} {unit} (S: {s_v} {unit})", align="left", font=("Courier", 10, "bold"))
                        t.goto(0, -h / 2 - 60)
                        t.write(f"Area: {b_v * h_v:.2f} {unit}²", align="center", font=("Courier", 14, "bold"))

                elif shape == "Circle":
                    r_v = screen.numinput("Circle", f"Radius ({unit}):", default=5)
                    if r_v:
                        sc = (W_HEIGHT / 4) / r_v
                        r = r_v * sc
                        t.penup()
                        t.goto(0, -r)
                        t.pendown()
                        t.circle(r)
                        t.penup()
                        t.goto(0, 10)
                        t.write(f"R: {r_v} {unit}", align="center", font=("Courier", 10, "bold"))
                        t.goto(0, -20)
                        t.write("360°", align="center", font=("Courier", 10, "bold"))
                        t.goto(0, -50)
                        t.write(f"Area: {math.pi * r_v ** 2:.2f} {unit}²", align="center", font=("Courier", 14, "bold"))


                elif shape not in [
                    "Triangle", "Circle", "Rectangle", "Square",
                    "Hexagon", "Parallelogram"
                ]:
                    polygon_name = shape_input.strip()

                    n_v = screen.numinput(
                        "Custom Polygon",
                        f"How many sides does '{polygon_name}' have? (3-100):",
                        default=5,
                        minval=3,
                        maxval=100
                    )

                    if n_v is not None:
                        n = int(n_v)

                        s_v = screen.numinput(
                            polygon_name,
                            f"Side length ({unit}):",
                            default=10,
                            minval=0.001
                        )

                        if s_v is not None and s_v > 0:
                            max_radius = min(W_WIDTH / 4, W_HEIGHT / 3)

                            points = []
                            for i in range(n):
                                angle = math.radians(-90 + i * 360 / n)
                                px = cx + max_radius * math.cos(angle)
                                py = cy + max_radius * math.sin(angle)
                                points.append((px, py))

                            t.color(SHAPE_COLOR)
                            t.pensize(2)
                            t.penup()
                            t.goto(points[0])
                            t.pendown()

                            for point in points[1:]:
                                t.goto(point)

                            t.goto(points[0])
                            t.penup()

                            perimeter = n * s_v
                            area = n * s_v**2 / (
                                4 * math.tan(math.pi / n)
                            )
                            interior_angle = (n - 2) * 180 / n

                            t.goto(cx, -max_radius - 30)
                            t.write(
                                f"{polygon_name}: {n} sides",
                                align="center",
                                font=("Courier", 12, "bold")
                            )

                            t.goto(cx, -max_radius - 55)
                            t.write(
                                f"Side: {s_v} {unit} | Angle: {interior_angle:.2f}°",
                                align="center",
                                font=("Courier", 10, "bold")
                            )

                            t.goto(cx, -max_radius - 80)
                            t.write(
                                f"Perimeter: {perimeter:.2f} {unit}",
                                align="center",
                                font=("Courier", 12, "bold")
                            )

                            t.goto(cx, -max_radius - 110)
                            t.write(
                                f"Area: {area:.2f} {unit}²",
                                align="center",
                                font=("Courier", 14, "bold")
                            )


            time.sleep(0.1)
        except (turtle.Terminator, tk.TclError):
            break

    try:
        screen.bye()
    except:
        pass
