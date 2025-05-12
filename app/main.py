from fasthtml.common import * # type: ignore
from colors import tailwind_colors
from functions import *

# for Docker
app, rt = fast_app(static_path="static") # type: ignore

# for local
# app, rt = fast_app(static_path="app/static") # type: ignore


default_header = Head(
                    Title("Color Converter"),
                    Meta(charset="UTF-8"),
                    Meta(name="viewport", content="width=device-width, initial-scale=1"),
                    Meta(name="description", content="insert page description for Search Engines"),
                    Meta(name="author", content="EvenMoreH"),
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
            Div(
                Span("Color Converter by "),
                A("EvenMoreH", href="https://github.com/EvenMoreH",
                cls="max-md:text-indigo-200 underline hover:text-indigo-200 hover:scale-105 transition-all duration-250"),
                cls="text-center fixed top-0 container p-2 bg-zinc-800 w-full rounded flex justify-center items-center space-x-1"
            ),
            # hex code div
            Div(
                Form(
                    Label("Enter HEX Color Code", cls="label1"),
                    Label("Example: #22c55e", cls="label2"),
                    Input(id="hex-color-input", name="color", type="text", cls="input"),
                    # hx_post="endpoint" instead of hx_post="/endpoint" uses relative path instead of absolute (allows proxy)
                    hx_post="hex_color",
                    hx_trigger="input",
                    hx_target="#hex-color-display",
                    cls="form1",
                ),
                # show color field
                Div(
                    id="hex-color-display",
                    cls="w-60 h-8 md:h-16 bg-transparent",
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
                    Label("Enter RGBA Color Code", cls="label1"),
                    Label("Example: 235,92,3,0.85", cls="label2"),
                    Input(id="rgba-color-input", name="color", type="text", cls="input"),
                    # hx_post="endpoint" instead of hx_post="/endpoint" uses relative path instead of absolute (allows proxy)
                    hx_post="rgba_color",
                    hx_trigger="input",
                    hx_target="#rgba-color-display",
                    cls="form2",
                ),
                # show color field
                Div(
                    id="rgba-color-display",
                    cls="w-60 h-8 md:h-16 bg-transparent",
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
                    Div(
                        Label(
                            "Enter",
                            Button("Tailwind Color Code",
                                hx_get="palette",
                                hx_trigger="click",
                                hx_target="#tailwind-palette",
                                hx_swap="innerHTML",
                                cls="max-md:text-indigo-200 pl-[6px] hover:text-indigo-200 hover:scale-105 transition-all 300ms"
                            ),
                            cls="flex items-center p-0.5 m-0.5 text-xl md:p-2 md:m-2 md:text-2xl"
                        )
                    ),
                    Label("Example: green-500", cls="label2"),
                    Input(id="tailwind-color-input", name="color", type="text", cls="input"),
                    # hx_post="endpoint" instead of hx_post="/endpoint" uses relative path instead of absolute (allows proxy)
                    hx_post="tailwind_color",
                    hx_trigger="input",
                    hx_target="#tailwind-color-display",
                    cls="form3",
                ),
                # show color field
                Div(
                    id="tailwind-color-display",
                    cls="w-60 h-8 md:h-16 bg-transparent",
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
            Div(
                id="tailwind-palette",
            ),
            # whole body css:
            cls="body"
        )
    )

@rt("/hex_color")
def post(color: str):
    color = string_cleaner(color, " ").lower()

    rgba_value = hex_to_rgba(color)
    tailwind_hex = tailwind_lstrip_name_lookup(color, tailwind_colors)

    return Div(
        id="hex-color-display",
        hx_swap_oob=True,
        cls="w-60 h-8 md:h-16",
        style=f"background-color: {rgba_value};",
        ), Div(
            f"{rgba_value}",
            id="rgba-color-value",
            hx_swap_oob=True,
            cls="w-60 h-6 text-gray-100 text-center mx-auto p-1",
        ), Div(
            f"Tailwind: {tailwind_hex}",
            id="hex-tailwind-color-value",
            hx_swap_oob=True,
            cls="w-60 h-6 text-gray-100 text-center mx-auto p-1",
        )

@rt("/rgba_color")
def post(color: str):
    color_clean = string_cleaner(color, " ()RGBArgba")

    hex_value = rgba_input_to_hex(color_clean)
    hex_value = hex_value.lower()

    tailwind_rgba = tailwind_name_lookup(hex_value, tailwind_colors)

    rgba_color = rgba_output_string(color_clean)

    return Div(
        id="rgba-color-display",
        hx_swap_oob=True,
        cls="w-60 h-8 md:h-16",
        style=f"background-color: {rgba_color};",
        ), Div(
            f"HEX: {hex_value}",
            id="hex-color-value",
            hx_swap_oob=True,
            cls="w-60 h-6 text-gray-100 text-center mx-auto p-1",
        ), Div(
            f"Tailwind: {tailwind_rgba}",
            id="rgba-tailwind-color-value",
            hx_swap_oob=True,
            cls="w-60 h-6 text-gray-100 text-center mx-auto p-1",
        ),

@rt("/tailwind_color")
def post(color: str):
    color = string_cleaner(color, " ").lower()

    tailwind_color = tailwind_value_lookup(color, tailwind_colors)

    rgba_value = hex_to_rgba(tailwind_color)

    return Div(
    id="tailwind-color-display",
    hx_swap_oob=True,
    cls="w-60 h-8 md:h-16",
    style=f"background-color: {tailwind_color};",
    ), Div(
        f"HEX: {tailwind_color}",
        id="hex-color-value",
        hx_swap_oob=True,
        cls="w-60 h-6 text-gray-100 text-center mx-auto p-1",
    ), Div(
        f"{rgba_value}",
        id="rgba-tailwind-color-value",
        hx_swap_oob=True,
        cls="w-60 h-6 text-gray-100 text-center mx-auto p-1",
    ),

@rt("/palette")
def get():
    return Div(
        Img(src="images/tailwind_palette.jpg",
            type="image/jpg",
            alt="test1",
        ),
        Button("Close",
            hx_get="close_modal",
            hx_target="#tailwind-palette",
            cls="close-palette"),
        cls="popup",
    )

@rt("/close_modal")
def get():
    return Div("")

if __name__ == '__main__':
    # Important: Use host='0.0.0.0' to make the server accessible outside the container
    serve(host='0.0.0.0', port=5033) # type: ignore