from PIL import Image
import cv2
# import numpy as np
from pillow_heif import register_heif_opener
import os
from logger import logger
import subprocess
from utills import compressSize


register_heif_opener()


# Get current working directing
BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


def CompressImage(file_name: str, ext: str) -> tuple[str, str, int]:
    FILE_PATH = f"{UPLOAD_DIR}/{file_name}"
    OUTPUT_PATH = os.path.join(BASE_DIR, f"downloads/{file_name}")

    # Read HEIC images using pyheif and convert to OpenCV format
    if ext == "heic":
        try:
            img = Image.open(FILE_PATH)
        except Exception as e:
            logger.error(f"Error: reading HEIC file: {e}")
            return ("Error reading HEIC file", "None", 0)
    else:
        # For other formats, read the image directly with OpenCV
        try:
            img = cv2.imread(FILE_PATH)
            # print("'''")
            # print(img)
            # print("'''")
        except Exception as e:
            logger.error("Error: Could not open or find the image")
            return ("Could not opnen or find the image", "None", 0)

    # Set the compression parameters for JPEG and PNG
    if ext in ["jpg", "jpeg"]:
        quality = 30
        compression_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        cv2.imwrite(OUTPUT_PATH, img, compression_params)

    elif ext == "png":
        quality = 30
        compression_params = [cv2.IMWRITE_PNG_COMPRESSION,
                              max(0, min(9, 9 - quality // 10))]
        cv2.imwrite(OUTPUT_PATH, img, compression_params)

    # Set the compression paramters for HEIC
    elif ext == "heic":
        quality = 75
        compress_size = compressSize(img.size, quality)

        img = img.resize(compress_size)
        img.save(OUTPUT_PATH, format="HEIF")

        img.close()

    else:
        logger.error(f"Error: unsupported file format -> {ext}")
        return ("Unsupported file format", "None", 0)

    # Gets new file size
    new_img_size = os.path.getsize(OUTPUT_PATH)

    return ("Success", file_name, new_img_size)


def CompressVideo(file_name: str) -> tuple[str, str, int]:
    FILE_PATH = f"{UPLOAD_DIR}/{file_name}"
    fname, _ = file_name.split('.')
    OUTPUT_PATH = os.path.join(BASE_DIR, f"downloads/{fname}.mp4")

   # Open the input video file
    cap = cv2.VideoCapture(FILE_PATH)

    # Check if the video was opened successfully
    if not cap.isOpened():
        logger.error("Error: Could not open video file")
        return ("Could not open video file", "Error", 0)

    # Gets the original fps of the uploaded video
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # crf = 21  # High quality
    crf = 28  # Low quality, where file size is important
    scale = 0.7
    scale_option = f"scale=trunc(iw*{scale}/2)*2:trunc(ih*{scale}/2)*2"

    # FFmpeg command to compress video and include audio
    command = [
        'ffmpeg', '-i', FILE_PATH,  # Input file
        '-vf', scale_option,  # Scale the video
        '-r', str(fps),  # Set frame rate
        '-vcodec', 'libx264',  # Use H.264 codec
        '-crf', str(crf),  # Compression quality
        '-acodec', 'aac',  # Audio codec (AAC is widely compatible)
        '-b:a', '128k',  # Set audio bitrate (128 kbps for good quality)
        '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
        # Set color space to ITU-R BT.709 (default for HD video)
        '-colorspace', '1',
        '-color_primaries', '1',          # Set color primaries to BT.709
        '-color_trc', '1',                # Set color transfer characteristic to BT.709
        # Fast start for .mp4 (improves playback on some devices)
        '-movflags', 'faststart',
        OUTPUT_PATH  # Output file path
    ]

    # Run the command
    try:
        completedProcess = subprocess.run(command)

        if completedProcess.returncode != 0:
            logger.error("Compression error: subprocess command failed")
            return ("Error: Compression Error", "none", 0)

    except Exception as e:
        logger.exception(e)

    new_video_size = os.path.getsize(OUTPUT_PATH)
    new_file_name = f"{fname}.mp4"

    return ("Success", new_file_name, new_video_size)
