def string_cleaner(input_string: str, characters_to_remove):
    """
    Remove specified characters from the input string.

    Parameters
    - input_string (str): The original string.
    - chars_to_remove (str): A string containing all characters to be removed.

    Returns
    - str: The modified string with specified characters removed.
    """

    for char in characters_to_remove:
        input_string = input_string.replace(char, '')
    return input_string


def hex_to_rgba(hex_color):
    # handles case when user clears input field
    if not hex_color:
        return ""

    # remove the hash symbol if present
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]

    # check if the length of the hex string is valid
    if len(hex_color) > 8:
        return "Invalid hex color format"

    if len(hex_color) in [3, 6, 8]:
        try:
            # if it's a 3-character hex code, expand it to 6
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])

            # if it's an 8-character hex code, extract the alpha value
            if len(hex_color) == 8:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                a = int(hex_color[6:8], 16) / 255.0  # convert to float (0.0 - 1.0)
            else:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                a = 1.0  # assuming full opacity by default

            result = f"RGBA({r},{g},{b},{a:.2f})"
            return result
        except:
            return "Invalid hex color format"
    else:
        return "Invalid hex color format"


def rgba_to_hex(r: int, g: int, b: int, a: float = 1.0):
    """
    Convert RGBA value to Hex color code.

    Parameters
    - r (int): Red component (0-255)
    - g (int): Green component (0-255)
    - b (int): Blue component (0-255)
    - a (float): Alpha component (0.0-1.0, optional)

    Returns
    - str: Hex color code
    """
    # ensure the RGBA values are within valid ranges
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    a = max(0.0, min(a, 1.0))

    # convert the RGB values to hexadecimal
    hex_r = format(r, '02X')
    hex_g = format(g, '02X')
    hex_b = format(b, '02X')

    # if alpha is not 1.0 (fully opaque), include it in the hex code
    if a < 1.0:
        hex_a = format(int(a * 255), '02X')
        return f"#{hex_r}{hex_g}{hex_b}{hex_a}"

    # return just the RGB part for fully opaque colors
    return f"#{hex_r}{hex_g}{hex_b}"


def rgba_input_to_hex(input_str: str):
    """
    Convert RGBA input string in the format 'RRR,GGG,BBB,A' to Hex color code.

    Parameters
    - input_str (str): Input string in the format 'r,g,b,a'

    Returns
    - str: Hex color code
    """
    # handles case when user clears input field
    if not input_str.strip():
        return ""

    try:
        # split the input string by commas and strip whitespace
        parts = [part.strip() for part in input_str.split(',')]

        if len(parts) == 3:
            # assume fully opaque alpha value (1.0) if user did not provide a value for it
            r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
            a = 1.0
        elif len(parts) == 4:
            r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
            a = float(parts[3])
        else:
            return ("Invalid RGB/RGBA format")

        # use rgba_to_hex function to handle conversion
        return rgba_to_hex(r, g, b, a)

    except:
        return ("Invalid RGB/RGBA format")


def tailwind_name_lookup(color: str, tailwind_colors):
    """
    Looks up tailwind color class in tailwind dictionary using hex code.

    Parameters
    - color (str): Input string in the format of tailwind hex code; example: #22c55e.
    - tailwind_colors: Dictionary of all built in tailwind colors.

    Returns
    - str: Tailwind color class name; example: green-500.
    """
    tailwind_class = "None"

    for key, value in tailwind_colors.items():
        if value == color:
            tailwind_class = key
            break
        else:
            tailwind_class = "None"

    return tailwind_class


def tailwind_lstrip_name_lookup(color: str, tailwind_colors):
    """
    1. Strips both input string and dictionary values of '#'
    2. Looks up tailwind color class in tailwind dictionary using hex code.

    Parameters
    - color (str): Input string in the format of tailwind hex code; example: #22c55e.
    - tailwind_colors: Dictionary of all built in tailwind colors.

    Returns
    - str: Tailwind color class name; example: green-500.
    """
    tailwind_class = "None"

    for key, value in tailwind_colors.items():
            if value.lstrip("#") == color.lstrip('#'):
                tailwind_class = key
                break
            else:
                tailwind_class = "None"

    return tailwind_class


def tailwind_value_lookup(color: str, tailwind_colors):
    """
    Looks up tailwind hex code in tailwind dictionary using tailwind class name.

    Parameters
    - color (str): Input string in the format of tailwind color class example: green-500.
    - tailwind_colors: Dictionary of all built in tailwind colors.

    Returns
    - str: Hex color code.
    - str: RGBA color code.
    """
    tailwind_color = "None"

    for key, value in tailwind_colors.items():
        if key == color:
            tailwind_color = value
            break
    else:
        tailwind_color = "Color not found"

    return tailwind_color



def rgba_output_string(input: str):
    """
    Takes in sanitized values and builds whole RGBA(R,B,G,A) string for display

    Parameters
    - input (str): sanitized color code

    Returns
    - rgba_string (str): ready to display string with RGBA(R,B,G,A) format
    """
    prefix = "RGBA("
    suffix = ")"
    rgba_string = prefix + input + suffix

    return rgba_string