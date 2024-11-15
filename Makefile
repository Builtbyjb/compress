css:
	npx tailwindcss -i ./static/input.css -o ./static/style.css --watch

run:
	python server.py

setup:
# Installs pngquant for png image compression (UNIX system)
	apt install pngquant
# Installs ffmpeg for video compression (UNIX system)
	apt install ffmpeg 

	
