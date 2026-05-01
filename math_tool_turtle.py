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
            # Ask for unit at the start of each loop
            unit = screen.textinput("Units", "Enter measurement unit (cm, m, in, ft):")
            if unit is None: unit = "units"

            cat_input = screen.textinput("Blueprint Category", "Choose: 2D or 3D (or 'Exit')")
            if cat_input is None or cat_input.strip().lower() == 'exit': break

            category = cat_input.strip().upper()
            cx, cy = 0, 0
            VIS_SIZE = W_WIDTH / 4
            VIS_OFF = VIS_SIZE * 0.3

            if category == "3D":
                shape_input = screen.textinput("3D Visualizer", "Cube, Cylinder, Pyramid")
                if not shape_input: continue
                shape = shape_input.strip().capitalize()
                t.clear()

                if shape == "Cube":
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

                elif shape == "Pyramid":
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

                elif shape == "Cylinder":
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

            elif category == "2D":
                shape_input = screen.textinput("2D Designer",
                                               "Triangle, Circle, Rectangle, Square, Hexagon, Parallelogram")
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

            time.sleep(0.1)
        except (turtle.Terminator, tk.TclError):
            break

    try:
        screen.bye()
    except:
        pass
