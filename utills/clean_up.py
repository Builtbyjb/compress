import threading
import subprocess
from datetime import datetime, timedelta
from logger import logger
import os

CURRENT_DIR = os.getcwd()


def UCleanUp(hrs: int):
    DIR = os.path.join(CURRENT_DIR, "uploads")
    COMMAND = ["rm -rf *.png"]

    del_time = datetime.now() + timedelta(seconds=hrs)

    while True:
        # new_time = current_time + timedelta(hours=hrs)
        current_time = datetime.now()

        if del_time == current_time:
            try:
                subprocess.run(COMMAND, cwd=DIR, shell=True)
                del_time += timedelta(seconds=10)
            except Exception as e:
                logger.error("Could not run subprocess")


def DCleanUp(hrs: int):
    DIR = os.path.join(CURRENT_DIR, "downloads")
    COMMAND = ["rm -rf *.png"]

    del_time = datetime.now() + timedelta(seconds=hrs)

    while True:
        # new_time = current_time + timedelta(hours=hrs)
        current_time = datetime.now()

        if del_time == current_time:
            try:
                subprocess.run(COMMAND, cwd=DIR, shell=True)
                del_time += timedelta(seconds=10)
            except Exception as e:
                logger.error("Could not run subprocess")


# Deletes files after a specified period of time
def fileCleanUp():
    f1 = threading.Thread(target=UCleanUp)
    f1.daemon = True

    f2 = threading.Thread(target=DCleanUp)
    f2.daemon = True

    # f1.start()
    # f2.start()
