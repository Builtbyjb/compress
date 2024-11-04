
ALLOWED_EXT = ["jpg", "jpeg", "png", "mkv", "mov", "mp4"]


# Valid file extention
def is_valid_ext(file_name: str) -> bool:
    ext_list = file_name.split(".")
    idx = len(ext_list) - 1
    if ext_list[idx] in ALLOWED_EXT:
        return True
    else:
        return False


ALLOWED_TYPE = ["image", "video"]


# Confirm content type
def is_valid_type(content_type: str) -> bool:
    type_s = content_type[0:5]
    if type_s in ALLOWED_TYPE:
        return True
    else:
        return False
