css:
	npx tailwindcss -i ./static/input.css -o ./static/style.css --watch

run:
	python server.py

# Installs ffmpeg for video compression
setup:
	apt install ffmpeg

	
