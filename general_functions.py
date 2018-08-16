def get_colors():
    colors_dict = {}
    
    lines = []
    with open("colors.txt", "r") as colors:
        for line in colors:
            lines.append(line)

    for line in lines:
        color, rgb_val = line.split(";")
        rgb_val = eval(rgb_val)
        colors_dict[color] = rgb_val

    return colors_dict
