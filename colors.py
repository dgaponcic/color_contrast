CONTRAST = 7
BREAK_POINT_LUMINANCE = 0.003

def get_color_val4luminance(val):
    return val / 12.92 if val <= 0.03928 else ((val + 0.055) / 1.055) ** 2.4 #https://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef

def get_denormalized_color(color):
    return {"r": color["r"] * 255, "g": color["g"] * 255, "b": color["b"] * 255}

def get_normalized_color(color):
    return {"r": color["r"] / 255, "g": color["g"] / 255, "b": color["b"] / 255}

def calculate_luminance(color):
    r = get_color_val4luminance(color["r"])
    g = get_color_val4luminance(color["g"])
    b = get_color_val4luminance(color["b"])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_contrast_luminance(luminance1, contrast):
    # https://www.w3.org/TR/2008/REC-WCAG20-20081211/#contrast-ratiodef

    # Light color divided by dark color
    # we can't now before hand what color in going to be lighter or darker so we compute both luminance
    
    light_luminance = contrast * (luminance1 + 0.05) - 0.05
    dark_luminance = (luminance1 + 0.05) / contrast - 0.05
    print(dark_luminance, light_luminance, luminance1)
    if luminance1 < light_luminance and light_luminance <= 1: 
        return light_luminance

    elif luminance1 > dark_luminance and dark_luminance >= 0: 
        return dark_luminance

    else:
        print(dark_luminance, light_luminance, luminance1)
        if luminance1 > 0.5:
            return 0
        return 1


def get_predefined_value(luminance2):
    print(luminance2)
    val = 0 if luminance2 < 0.5 else 1
    return {"r": val, "g": None, "b": None}


def get_initial_value(val):
    if val < BREAK_POINT_LUMINANCE: 
        return val * 12.92
    else:
        return val ** (5 / 12) * 1.055 - 0.055
        

def compute_light_color(color2, luminance2):
    b, g = 256, -1
    while g < 0 and b > 0:
        b -= 1
        normalized_b = b / 255
        g = (luminance2 - 0.2126 * color2["r"] - 0.0722 * normalized_b) / 0.7152
        print("g", g)

    return {"r": color2["r"], "g": get_initial_value(g), "b": get_initial_value(b / 255)}


def compute_dark_color(color2, luminance2):
    b, g = -1, -1
    while g < 0:
        b += 1
        normalized_b = b / 255
        g = (luminance2 - 0.2126 * color2["r"] - 0.0722 * normalized_b) / 0.7152
    return {"r": color2["r"], "g": get_initial_value(g), "b": get_initial_value(b / 255)}


def get_contrast_color(luminance2, color1):
    color2 = get_predefined_value(luminance2)
    return compute_light_color(color2, luminance2) if color2["r"] == 1 else compute_dark_color(color2, luminance2)

if __name__ == "__main__":
    initial_color1 = {"r": 255, "g": 0, "b": 0}
    color1 = get_normalized_color(initial_color1)
    luminance1 = calculate_luminance(color1)
    luminance2 = get_contrast_luminance(luminance1, CONTRAST)
    color2 = get_contrast_color(luminance2, color1)
    final_color = get_denormalized_color(color2)

    print(final_color)
