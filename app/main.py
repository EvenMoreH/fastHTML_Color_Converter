from fasthtml.common import * # type: ignore
from colors import tailwind_colors
from functions import *

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


@rt("/")
def get():
    return Html(
        default_header,
        Body(
            # hex code div
            Div(
                Form(
                    Label("Enter HEX Color Code", cls="p-2 m-2 text-2xl"),
                    Label("Example: #22c55e", cls="text-xl text-gray-400 pb-1 mb-1"),
                    Input(id="hex-color-input", name="color", type="text", cls="input"),
                    hx_post="/hex_color",
                    hx_trigger="input",
                    hx_target="#hex-color-display",
                    cls="p-2 mx-2 flex flex-col container justify-center items-center",
                ),
                # show color field
                Div(
                    id="hex-color-display",
                    cls="w-60 h-16 bg-transparent",
                ),
                # show rgba code
                Div(
                    id="rgba-color-value",
                ),
                # show tailwind class if match is found
                Div(
                    id="hex-tailwind-color-value",
                ),
                cls="div",
            ),
            # rgba div
            Div(
                Form(
                    Label("Enter RGBA Color Code", cls="p-2 m-2 text-2xl"),
                    Label("Example: 235,92,3,0.85", cls="text-xl text-gray-400 pb-1 mb-1"),
                    Input(id="rgba-color-input", name="color", type="text", cls="input"),
                    hx_post="/rgba_color",
                    hx_trigger="input",
                    hx_target="#rgba-color-display",
                    cls="p-2 mx-2 flex flex-col container justify-center items-center",
                ),
                # show color field
                Div(
                    id="rgba-color-display",
                    cls="w-60 h-16 bg-transparent",
                ),
                # show hex code
                Div(
                    id="hex-color-value",
                ),
                # show tailwind class if match is found
                Div(
                    id="rgba-tailwind-color-value",
                ),
                cls="div",
            ),
            # tailwind div
            Div(
                Form(
                    Label("Enter Tailwind Color Code", cls="p-2 m-2 text-2xl"),
                    Label("Example: green-500", cls="text-xl text-gray-400 pb-1 mb-1"),
                    Input(id="tailwind-color-input", name="color", type="text", cls="input"),
                    hx_post="/tailwind_color",
                    hx_trigger="input",
                    hx_target="#tailwind-color-display",
                    cls="p-2 mx-2 flex flex-col container justify-center items-center",
                ),
                # show color field
                Div(
                    id="tailwind-color-display",
                    cls="w-60 h-16 bg-transparent",
                ),
                # show hex code
                Div(
                    id="hex-color-value",
                ),
                # show rgba code
                Div(
                    id="rgba-color-valuee",
                ),
                cls="div-center",
            ),
            # whole body css:
            cls="body"
        )
    )

@rt("/hex_color")
def post(color: str):
    # clean up the string and handle conversion to RGBA
    color = color.lower()
    color = string_cleaner(color, " ")
    rgba_value = hex_to_rgba(color)

    # strip the # if present and lookup tailwind class
    color = string_cleaner(color, "#")
    for key, value in tailwind_colors.items():
            if value.lstrip("#") == color:
                tailwind_hex = key
                print(tailwind_hex)
                break
            else:
                tailwind_hex = "None"

    return Div(
        id="hex-color-display",
        hx_swap_oob=True,
        cls="w-60 h-16",
        style=f"background-color: {rgba_value};",
        ), Div(
            f"{rgba_value}",
            id="rgba-color-value",
            hx_swap_oob=True,
            cls="w-60 h-12 text-gray-100 text-center mx-auto p-1",
        ), Div(
            f"Tailwind: {tailwind_hex}",
            id="hex-tailwind-color-value",
            hx_swap_oob=True,
            cls="w-60 h-6 text-gray-100 text-center mx-auto p-1",
        )

@rt("/rgba_color")
def post(color: str):
    # clean up the string for conversion
    color_to_convert = color
    converted_color = string_cleaner(color_to_convert, " ()RGBArgba")
    # convert to hex
    hex_value = rgba_input_to_hex(converted_color)
    # lookup the tailwind class if any
    hex_value_low = hex_value.lower()
    for key, value in tailwind_colors.items():
        if value == hex_value_low:
            tailwind_rgba = key
            break
        else:
            tailwind_rgba = "None"

    # build RGBA string output to look nice
    prefix = "RGBA("
    suffix = ")"
    rgba_color = prefix + converted_color + suffix

    return Div(
        id="rgba-color-display",
        hx_swap_oob=True,
        cls="w-60 h-16",
        style=f"background-color: {rgba_color};",
        ), Div(
            f"HEX: {hex_value}",
            id="hex-color-value",
            hx_swap_oob=True,
            cls="w-60 h-12 text-gray-100 text-center mx-auto p-1",
        ), Div(
            f"Tailwind: {tailwind_rgba}",
            id="rgba-tailwind-color-value",
            hx_swap_oob=True,
            cls="w-60 h-6 text-gray-100 text-center mx-auto p-1",
        ),

@rt("/tailwind_color")
def post(color: str):
    color = color.lower()
    color = string_cleaner(color, " ")

    tailwind_color = "None"

    for key, value in tailwind_colors.items():
        if key == color:
            tailwind_color = value
            break
    else:
        tailwind_color = "Color not found in the dictionary."

    print(tailwind_color)
    rgba_value = hex_to_rgba(tailwind_color)
    print(rgba_value)


    return Div(
    id="tailwind-color-display",
    hx_swap_oob=True,
    cls="w-60 h-16",
    style=f"background-color: {tailwind_color};",
    ), Div(
        f"HEX: {tailwind_color}",
        id="hex-color-value",
        hx_swap_oob=True,
        cls="w-60 h-12 text-gray-100 text-center mx-auto p-1",
    ), Div(
        f"{rgba_value}",
        id="rgba-tailwind-color-value",
        hx_swap_oob=True,
        cls="w-60 h-6 text-gray-100 text-center mx-auto p-1",
    ),


serve()

# if __name__ == '__main__':
#     # Important: Use host='0.0.0.0' to make the server accessible outside the container
#     serve(host='0.0.0.0', port=5033) # type: ignore