if __name__ == "__main__":

 import math
while True:
    unit = input("Enter the unit of measurement (cm, m, in, ft, or a custom unit):")
    Shape_type = str(input("Shape type (3D or 2D): ")).strip().upper()

    if Shape_type == "2D":
        Shape_2D = str(input("Shape (Triangle, Circle, Rectangle, Square, Parallelogram, Hexagon, a custom polygon or Exit): ")).strip().capitalize()

        if Shape_2D == "Triangle":
            Base = float(input(f"Base({unit}): "))
            Height = float(input(f"Height({unit}): "))
            Hypotenuse = math.sqrt(Base ** 2 + Height ** 2)
            print(f"> Hypotenuse: {Hypotenuse:.2f} {unit}")
            angle_rad = math.acos(Base / Hypotenuse)
            angle_deg = math.degrees(angle_rad)
            print(f"> Base angle: {angle_deg:.2f} degrees")
            print(f"> Acute angle: {90 - angle_deg:.2f} degrees")

        elif Shape_2D == "Circle":
            Radius = float(input(f"Radius({unit}): "))
            area = math.pi * (Radius ** 2)
            circumference = 2 * math.pi * Radius
            print(f"> Circumference: {circumference:.2f} {unit}")
            print(f"> Area: {area:.2f} {unit}²")

        elif Shape_2D == "Rectangle":
            Length = float(input(f"Length ({unit}): "))
            Width = float(input(f"Width ({unit}): "))
            area = Length * Width
            perimeter = 2 * (Length + Width)
            print(f"> Perimeter: {perimeter:.2f} {unit}")
            print(f"> Area: {area:.2f} {unit}²")

        elif Shape_2D == "Square":
            Side = float(input(f"Side ({unit}): "))
            print(f"> Perimeter: {4 * Side:.2f} {unit}")
            print(f"> Area: {Side ** 2:.2f} {unit}²")

        elif Shape_2D == "Parallelogram":
            Base = float(input(f"Base({unit}): "))
            Height = float(input(f"Height ({unit}): "))
            Side_B = float(input(f"Side length (the slanted side)({unit}): "))
            print(f"> Area: {Base * Height:.2f} {unit}²")
            print(f"> Perimeter: {2 * (Base + Side_B):.2f} {unit}")

        elif Shape_2D == "Hexagon":
            Side = float(input(f"Side length ({unit}): "))
            area = (3 * math.sqrt(3) / 2) * (Side ** 2)
            print(f"> Area: {area:.2f} {unit}²")
            print(f"> Perimeter: {6 * Side:.2f} {unit}")

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
                print(f"> Total Area: {area:.2f}²")
                print(f"> Perimeter: {num_sides * side_length:.2f} {unit}")
            except ValueError:
                print("> Please enter valid numbers for sides and length.")

    elif Shape_type == "3D":
        Shape_3D = str(input("Shape (Cube, Cuboid, Sphere, Cylinder, Pyramid, Cone or Exit): ")).strip().capitalize()
        try:
            if Shape_3D == "Cube":
                Length = float(input(f"Length of any edge ({unit}): "))
                Volume = Length ** 3
                print(f"> Volume: {Volume:.2f} {unit}³")

            elif Shape_3D == "Cuboid":
                Length = float(input(f"Length of Cuboid ({unit}): "))
                Width = float(input(f"Width of Cuboid ({unit}): "))
                Height = float(input(f"Height of Cuboid ({unit}): "))
                Volume = Length * Width * Height
                print(f"> Volume: {Volume:.2f} {unit}³ ")

            elif Shape_3D == "Sphere":
                Radius = float(input(f"Radius ({unit}): "))
                Volume = 4 / 3 * math.pi * (Radius ** 3)
                print(f"> Volume: {Volume:.2f} {unit}³")

            elif Shape_3D == "Cylinder":
                Radius = float(input(f"Radius of the base or top ({unit}): "))
                Height = float(input(f"Height of Cylinder ({unit}): "))
                Volume = math.pi * (Radius ** 2) * Height
                print(f"> Volume: {Volume:.2f} {unit}³")

            elif Shape_3D == "Pyramid":
                Length = float(input(f"Length of Base ({unit}): "))
                Width = float(input(f"Width of Base ({unit}): "))
                Height = float(input(f"Vertical height ({unit}): "))
                Volume = Length * Width * Height / 3
                print(f"> Volume: {Volume:.2f} {unit}³")

            elif Shape_3D == "Cone":
                Radius = float(input(f"Radius of the base ({unit}): "))
                Height = float(input(f"Vertical height ({unit}): "))
                Volume = (1/3) * math.pi * (Radius ** 2) * Height
                print(f"> Volume: {Volume:.2f} {unit}³")


            elif Shape_3D == "Exit":
                print("Goodbye")
                break

            elif Shape_3D == "":
                print("> Please enter a valid name for your shape.")
        except ValueError:
            print("> Error: Please enter numbers only for dimensions!")

