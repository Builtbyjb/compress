from PIL import Image
import os
from utills import compressSize

# Get current working directing
BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


def CompressImage(file_name) -> tuple:
    filename = f"{UPLOAD_DIR}/{file_name}"
    OUTPUT_DIR = os.path.join(BASE_DIR, f"compressed/{file_name}")

    try:
        img = Image.open(filename)
    except:
        return ("Compression Error", "Error", "Error")

    format = img.format
    if format == "JPG" or format == "JPEG":
        quality = 50
    elif format == "PNG":
        quality = 75
    else:
        quality = 75

    compress_size = compressSize(img.size, quality)

    img = img.resize(compress_size)
    img.save(OUTPUT_DIR, format=format)

    img.close()

    return ("Compression Successful", file_name, compress_size)


def CompressVideo(videoFIle):
    ...
