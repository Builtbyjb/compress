from PIL import Image
import os

# Get current working directing
BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


def CompressImage(file_name, file_size) -> tuple:

    filename = f"{UPLOAD_DIR}/{file_name}"
    OUTPUT_DIR = os.path.join(BASE_DIR, f"compressed/{file_name}")

    # Open the image file
    img = Image.open(filename)

    # Get the image format
    format = img.format
    # print(format)
    # print(file_size)

    # Apply compression based on format
    if format == 'JPEG':
        # img.save(OUTPUT_DIR, format=format, quality="web_low", optimize=True)
        img = img.resize(file_size)
        img.save(OUTPUT_DIR, format=format)

    elif format == 'PNG':
        img = img.resize(file_size)
        # img.save(OUTPUT_DIR, format=format, optimize=True, compress_level=5)
        img.save(OUTPUT_DIR, format=format)

    elif format == 'GIF':
        # For GIF, we reduce the number of colors to limit file size
        img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
        img.save(OUTPUT_DIR, optimize=True)

    img.close()

    return (file_name, img.size)


def CompressVideo(videoFIle):
    ...
