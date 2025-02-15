from fasthtml.common import * # type: ignore
import re

# for Docker
# app, rt = fast_app(static_path="static") # type: ignore

# for local
app, rt = fast_app(static_path="app/static") # type: ignore


default_header = Head(
                    Title("Color Converter"),
                    Meta(name="viewport", content="width=device-width, initial-scale=1"),
                    Script(src="https://unpkg.com/htmx.org"),
                    Link(rel="stylesheet", href="css/tailwind.css"),
                    Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
                    Link(rel="icon", href="images/favicon.png", type="image/png"),
                )

def string_cleaner(input_string: str):
    """
    Remove specified characters from the input string.

    Parameters:
    - input_string (str): The original string.
    - chars_to_remove (str): A string containing all characters to be removed.

    Returns:
    - str: The modified string with specified characters removed.
    """
    characters_to_remove = " ()RGBArgba"

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

    Parameters:
    r (int): Red component (0-255)
    g (int): Green component (0-255)
    b (int): Blue component (0-255)
    a (float): Alpha component (0.0-1.0, optional)

    Returns:
    str: Hex color code
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

    Parameters:
    input_str (str): Input string in the format 'r,g,b,a'

    Returns:
    str: Hex color code
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
            return ('Input must be in the format "R,G,B" or "R,G,B,A"')

        # use rgba_to_hex function to handle conversion
        return rgba_to_hex(r, g, b, a)

    except:
        return ('Input must be in the format "R,G,B" or "R,G,B,A"')



@rt("/")
def get():
    return Html(
        default_header,
        Body(
            # hex code div
            Div(
                Form(
                    Label("Enter HEX Color Code", cls="p-2 m-2 text-2xl"),
                    Label("Example: #22c55e", cls="text-xl text-gray-300 pb-1 mb-1"),
                    Input(id="hex-color-input", name="color", type="text", cls="input"),
                    hx_post="/hex_color",
                    hx_trigger="input",
                    hx_target="#hex-color-display",
                    cls="p-2 mx-2 flex flex-col container justify-center items-center",
                ),
                Div(
                    id="hex-color-display",
                    cls="w-60 h-16 bg-transparent",
                ),
                Div(
                    id="rgba-color-value",
                ),
                cls="div",
            ),
            # rgba div
            Div(
                Form(
                    Label("Enter RGBA Color Code", cls="p-2 m-2 text-2xl"),
                    Label("Example: 235,92,3,0.85", cls="text-xl text-gray-300 pb-1 mb-1"),
                    Input(id="rgba-color-input", name="color", type="text", cls="input"),
                    hx_post="/rgba_color",
                    hx_trigger="input",
                    hx_target="#rgba-color-display",
                    cls="p-2 mx-2 flex flex-col container justify-center items-center",
                ),
                Div(
                    id="rgba-color-display",
                    cls="w-60 h-16 bg-transparent",
                ),
                Div(
                    id="hex-color-value",
                ),
                cls="div",
            ),
            # whole body css:
            cls="body"
        )
    )

@rt("/hex_color")
def post(color: str):
    rgba_value = hex_to_rgba(color)

    return Div(
        id="hex-color-display",
        hx_swap_oob=True,
        cls="w-60 h-16",
        style=f"background-color: {color};",
        ), Div(
            f"{rgba_value}",
            id="rgba-color-value",
            hx_swap_oob=True,
            cls="w-60 h-16 text-gray-100 text-center mx-auto p-1",
        )

@rt("/rgba_color")
def post(color: str):
    color_to_convert = color
    converted_color = string_cleaner(color_to_convert)

    hex_value = rgba_input_to_hex(converted_color)

    prefix = "RGBA("
    suffix = ")"
    rgba_color = prefix + converted_color + suffix

    return Div(
        id="rgba-color-display",
        hx_swap_oob=True,
        cls="w-60 h-16",
        style=f"background-color: {rgba_color};",
        ), Div(
            f"{hex_value}",
            id="hex-color-value",
            hx_swap_oob=True,
            cls="w-60 h-16 text-gray-100 text-center mx-auto p-1",
        )


serve()

# if __name__ == '__main__':
#     # Important: Use host='0.0.0.0' to make the server accessible outside the container
#     serve(host='0.0.0.0', port=5033) # type: ignore