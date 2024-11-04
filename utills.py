
ALLOWED_EXT = ["jpg", "jpeg", "png", "mkv", "mov", "mp4"]


# Valid file extention
def ValidateExtention(file_name: str) -> tuple:
    ext_list = file_name.lower().split(".")
    idx = len(ext_list) - 1
    if ext_list[idx] in ALLOWED_EXT:
        return (True, ext_list[idx])
    else:
        return (False, "")


ALLOWED_TYPE = ["image", "video"]


# Confirm content type
def ValidateType(content_type: str) -> tuple:
    type_s = content_type[0:5].lower()
    if type_s in ALLOWED_TYPE:
        return (True, type_s)
    else:
        return (False, "")
