from PIL import Image
import cv2
from pillow_heif import register_heif_opener
import os
from logger import logger
import subprocess
from utills.utills import compressSize, registerDownloadFile
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from database.schema import File
from sqlmodel import Session
from database.database import get_session
from dotenv import load_dotenv


database = Annotated[Session, Depends(get_session)]
register_heif_opener()
load_dotenv()


EXPIRED_AT = int(os.getenv("EXPIRED_AT"))

# Get current working directing
BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


def CompressImage(file_name: str, ext: str, db: database) -> tuple[str, str, int]:
    FILE_PATH = f"{UPLOAD_DIR}/{file_name}"
    OUTPUT_PATH = os.path.join(BASE_DIR, f"downloads/{file_name}")

    # Compress jpeg and jpg images
    if ext in ["jpg", "jpeg"]:
        try:
            img = cv2.imread(FILE_PATH)
        except Exception as e:
            logger.error("Could not open or find the JPG/JPEG image")
            return ("Could not opnen or find the JPG/JPEG image", "None", 0)

        quality = 30

        compression_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        success = cv2.imwrite(OUTPUT_PATH, img, compression_params)

        if not success:
            logger.error("Could not save file")
            return ("Could not save file", "None", 0)

    # Compress png images
    elif ext == "png":

        # Use pngquant to compress png files
        command = ['pngquant', '--force', '--output',
                   OUTPUT_PATH, FILE_PATH]

        # Run the command
        try:
            completedProcess = subprocess.run(command, check=True)

            if completedProcess.returncode != 0:
                logger.error("Compression error: subprocess command failed")
                return ("Error: Compression Error", "none", 0)

        except Exception as e:
            logger.exception(e)

        # Compress HEIC images
    elif ext == "heic":
        try:
            # img = cv2.imread(FILE_PATH)
            img = Image.open(FILE_PATH)
        except Exception as e:
            logger.error(f"Error: reading HEIC image: {e}")
            return ("Error reading HEIC image", "None", 0)

        quality = 70
        compress_size = compressSize(img.size, quality)

        img = img.resize(compress_size)
        img.save(OUTPUT_PATH, format="HEIF", optimize=True)

        img.close()

    else:
        logger.error(f"Error: unsupported file format -> {ext}")
        return ("Unsupported file format", "None", 0)

    uploaded_time = datetime.now()
    expiring_time = datetime.now() + timedelta(hours=EXPIRED_AT)

    download_file = File(
        name=file_name,
        uploaded=uploaded_time.strftime("%Y-%m-%d %H:%M"),
        expired=expiring_time.strftime("%Y-%m-%d %H:%M")
    )

    registerDownloadFile(download_file, db)

    # Gets new file size
    new_img_size = os.path.getsize(OUTPUT_PATH)

    return ("Success", file_name, new_img_size)


def CompressVideo(file_name: str, db: database) -> tuple[str, str, int]:
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
        completedProcess = subprocess.run(command, check=True)

        if completedProcess.returncode != 0:
            logger.error("Compression error: subprocess command failed")
            return ("Error: Compression Error", "none", 0)

    except Exception as e:
        logger.exception(e)

    uploaded_time = datetime.now()
    expiring_time = datetime.now() + timedelta(hours=EXPIRED_AT)

    new_file_name = f"{fname}.mp4"

    download_file = File(
        name=new_file_name,
        uploaded=uploaded_time.strftime("%Y-%m-%d %H:%M"),
        expired=expiring_time.strftime("%Y-%m-%d %H:%M")
    )

    registerDownloadFile(download_file, db)

    new_video_size = os.path.getsize(OUTPUT_PATH)

    return ("Success", new_file_name, new_video_size)
