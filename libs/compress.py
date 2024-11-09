from PIL import Image
from pillow_heif import register_heif_opener
import os
from utills import compressSize


register_heif_opener()


# Get current working directing
BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


def CompressImage(file_name) -> tuple[str, str, int]:
    filename = f"{UPLOAD_DIR}/{file_name}"
    OUTPUT_DIR = os.path.join(BASE_DIR, f"compressed/{file_name}")

    try:
        img = Image.open(filename)
    except:
        return ("Compression Error", "Error", 0)

    format = img.format

    if format == "JPG" or format == "JPEG":
        quality = 50
    elif format == "PNG":
        quality = 75
    elif format == "HEIF":
        quality = 50

    compress_size = compressSize(img.size, quality)

    img = img.resize(compress_size)
    img.save(OUTPUT_DIR, format=format)

    img.close()

    return ("Compression Successful", file_name, compress_size)


def CompressVideo(videoFIle):
    ...
