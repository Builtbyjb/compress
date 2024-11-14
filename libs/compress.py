from PIL import Image
import cv2
import numpy as np
from pillow_heif import register_heif_opener
import os
from logger import logger
import pyheif
from utills import compressSize


register_heif_opener()


# Get current working directing
BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


def CompressImage(file_name, ext) -> tuple[str, str, int]:
    filename = f"{UPLOAD_DIR}/{file_name}"
    OUTPUT_PATH = os.path.join(BASE_DIR, f"downloads/{file_name}")

    # Read HEIC images using pyheif and convert to OpenCV format
    if ext == "heic":
        try:
            img = Image.open(filename)
        except Exception as e:
            logger.error(f"Error: reading HEIC file: {e}")
            return ("Error reading HEIC file", "None", 0)
    else:
        # For other formats, read the image directly with OpenCV
        try:
            img = cv2.imread(filename)
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


def CompressVideo(file_name):
    filename = f"{UPLOAD_DIR}/{file_name}"
    fn, _ = file_name.split('.')
    OUTPUT_PATH = os.path.join(BASE_DIR, f"downloads/{fn}.mp4")

    codec = 'XVID'
    scale = 0.5

    # Open the input video file
    cap = cv2.VideoCapture(filename)

    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get the original video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    original_fps = int(cap.get(cv2.CAP_PROP_FPS))

    fps = original_fps

    # Set the codec and create VideoWriter for the output video
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps,
                          (int(width * scale), int(height * scale)))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame
        frame = cv2.resize(frame, (int(width * scale), int(height * scale)))

        # Write the compressed frame to the output video
        out.write(frame)

    # Release resources
    cap.release()
    out.release()
    print("Video compression completed.")

    new_video_size = os.path.getsize(OUTPUT_PATH)

    return ("Success", file_name, new_video_size)
