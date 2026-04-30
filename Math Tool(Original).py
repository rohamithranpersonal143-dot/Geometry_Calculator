import math

while True:
    Shape_type = str(input("Shape type (3D or 2D): ")).strip().upper()

    if Shape_type == "2D":
        Shape_2D = str(input("Shape (Triangle, Circle, Rectangle, Square, Parallelogram, Hexagon or Exit): ")).strip().capitalize()

        if Shape_2D == "Triangle":
            Base = float(input("Base: "))
            Height = float(input("Height: "))
            Hypotenuse = math.sqrt(Base ** 2 + Height ** 2)
            print(f"> Hypotenuse: {Hypotenuse:.2f}")
            angle_rad = math.acos(Base / Hypotenuse)
            angle_deg = math.degrees(angle_rad)
            print(f"> Base angle: {angle_deg:.2f} degrees")
            print(f"> Acute angle: {90 - angle_deg:.2f} degrees")

        elif Shape_2D == "Circle":
            Radius = float(input("Radius: "))
            area = math.pi * (Radius ** 2)
            circumference = 2 * math.pi * Radius
            print(f"> Circumference: {circumference:.2f}")
            print(f"> Area: {area:.2f}")

        elif Shape_2D == "Rectangle":
            Length = float(input("Length: "))
            Width = float(input("Width: "))
            area = Length * Width
            perimeter = 2 * (Length + Width)
            print(f"> Perimeter: {perimeter:.2f}")
            print(f"> Area: {area:.2f}")

        elif Shape_2D == "Square":
            Side = float(input("Side: "))
            print(f"> Perimeter: {4 * Side:.2f}")
            print(f"> Area: {Side ** 2:.2f}")

        elif Shape_2D == "Parallelogram":
            Base = float(input("Base: "))
            Height = float(input("Height: "))
            Side_B = float(input("Side length (the slanted side): "))
            print(f"> Area: {Base * Height:.2f}")
            print(f"> Perimeter: {2 * (Base + Side_B):.2f}")

        elif Shape_2D == "Hexagon":
            Side = float(input("Side length: "))
            area = (3 * math.sqrt(3) / 2) * (Side ** 2)
            print(f"> Area: {area:.2f}")
            print(f"> Perimeter: {6 * Side:.2f}")

        elif Shape_2D == "Exit":
            print("Goodbye")
            break

        elif Shape_2D == "":
            print("> Please enter a valid name for your shape.")

        else:
            try:
                num_sides = int(input(f"How many sides does a {Shape_2D} have? "))
                side_length = float(input("What is the length of each side? "))
                if num_sides < 3:
                    print("> A polygon must have at least 3 sides.")
                    continue
                interior_angle = ((num_sides - 2) * 180) / num_sides
                area = (num_sides * side_length ** 2) / (4 * math.tan(math.pi / num_sides))
                print(f"> Each interior angle: {interior_angle:.2f} degrees")
                print(f"> Total Area: {area:.2f}")
                print(f"> Perimeter: {num_sides * side_length:.2f}")
            except ValueError:
                print("> Please enter valid numbers for sides and length.")

    elif Shape_type == "3D":
        Shape_3D = str(input("Shape (Cube, Cuboid, Sphere, Cylinder, Pyramid, Cone or Exit): ")).strip().capitalize()
        try:
            if Shape_3D == "Cube":
                Length = float(input("Length of any edge: "))
                Volume = Length ** 3
                print(f"> Volume: {Volume:.2f}")

            elif Shape_3D == "Cuboid":
                Length = float(input("Length of Cuboid: "))
                Width = float(input("Width of Cuboid: "))
                Height = float(input("Height of Cuboid: "))
                Volume = Length * Width * Height
                print(f"> Volume: {Volume:.2f}")

            elif Shape_3D == "Sphere":
                Radius = float(input("Radius: "))
                Volume = 4 / 3 * math.pi * (Radius ** 3)
                print(f"> Volume: {Volume:.2f}")

            elif Shape_3D == "Cylinder":
                Radius = float(input("Radius of the base or top: "))
                Height = float(input("Height of Cylinder: "))
                Volume = math.pi * (Radius ** 2) * Height
                print(f"> Volume: {Volume:.2f}")

            elif Shape_3D == "Pyramid":
                Length = float(input("Length of Base: "))
                Width = float(input("Width of Base: "))
                Height = float(input("Vertical height: "))
                Volume = Length * Width * Height / 3
                print(f"> Volume: {Volume:.2f}")

            elif Shape_3D == "Cone":
                Radius = float(input("Radius of the base: "))
                Height = float(input("Vertical height: "))
                Volume = (1/3) * math.pi * (Radius ** 2) * Height
                print(f"> Volume: {Volume:.2f}")


            elif Shape_3D == "Exit":
                print("Goodbye")
                break

            elif Shape_3D == "":
                print("> Please enter a valid name for your shape.")
        except ValueError:
            print("> Error: Please enter numbers only for dimensions!")

