import threading
import subprocess
from datetime import datetime
from logger import logger
import os
from database.database import get_session, UploadFiles, DownloadFiles
from sqlmodel import select
from utills.utills import FormatTime


CURRENT_DIR = os.getcwd()


# Cleans up uploads directory
def UCleanUp():
    DIR = os.path.join(CURRENT_DIR, "uploads")
    print("...")
    print("Starting up UCleanUp...")
    print("...")

    while True:
        with next(get_session()) as db:
            upload_files = db.exec(select(UploadFiles)).all()

            for file in upload_files:
                current_time = FormatTime(datetime.now())
                if current_time == file.expired:
                    COMMAND = [f"rm -rf {file.name}"]

                    try:
                        subprocess.run(COMMAND, cwd=DIR, shell=True)
                    except Exception as e:
                        logger.error("Could not run subprocess")


# Cleans up downloads directory
def DCleanUp():
    DIR = os.path.join(CURRENT_DIR, "downloads")
    print("...")
    print("Starting up DCleanUp...")
    print("...")

    while True:
        with next(get_session()) as db:
            download_files = db.exec(select(DownloadFiles)).all()

            for file in download_files:
                current_time = FormatTime(datetime.now())
                if current_time == file.expired:
                    COMMAND = [f"rm -rf {file.name}"]

                try:
                    subprocess.run(COMMAND, cwd=DIR, shell=True)
                except Exception as e:
                    logger.error("Could not run subprocess")


# Deletes files after a specified period of time
def fileCleanUp():
    f1 = threading.Thread(target=UCleanUp)
    f1.daemon = True

    f2 = threading.Thread(target=DCleanUp)
    f2.daemon = True

    f1.start()
    f2.start()
