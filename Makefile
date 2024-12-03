css:
	npx tailwindcss -i ./static/input.css -o ./static/style.css --watch

dev:
	uvicorn server:app --reload --host 127.0.0.1 --port 8010

setup:
# Installs pngquant for png image compression (UNIX system)
	apt install pngquant
# Installs ffmpeg for video compression (UNIX system)
	apt install ffmpeg 

	
