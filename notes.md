# Port:
5033

# Docker image build command:
docker build -t image-color-converter-img .

# Docker image run command:
docker run -p 5033:5033 image-color-converter-img
<!-- To run without a console use -d argument -->
docker run -d -p 5033:5033 image-color-converter-img
hub
# Project Tree
📦fastHTML_Color_Converter
 ┣ 📂app
 ┃ ┣ 📂static
 ┃ ┃ ┣ 📂css
 ┃ ┃ ┃ ┣ 📜input.css
 ┃ ┃ ┃ ┗ 📜tailwind.css
 ┃ ┃ ┗ 📂images
 ┃ ┃ ┃ ┣ 📜favicon.ico
 ┃ ┃ ┃ ┣ 📜favicon.png
 ┃ ┃ ┃ ┗ 📜tailwind_palette.jpg
 ┃ ┣ 📜colors.py
 ┃ ┣ 📜functions.py
 ┃ ┗ 📜main.py
 ┣ 📜.gitignore
 ┣ 📜Dockerfile
 ┣ 📜notes.md
 ┣ 📜requirements.txt
 ┗ 📜tailwind.config.js


# Tailwind
<!-- initialize tailwind config for given project -->
C:\Compilers\Tailwind\tailwindcss-windows-x64.exe init

<!-- build tailwind.css output from specified input.css with --watch flag for rebuilding -->
C:\Compilers\Tailwind\tailwindcss-windows-x64.exe -i app/static/css/input.css -o app/static/css/tailwind.css --watch

<!-- build tailwind.css output from specified input.css with --minify flag to conserve space for docker -->
C:\Compilers\Tailwind\tailwindcss-windows-x64.exe -i app/static/css/input.css -o app/static/css/tailwind.css --minify