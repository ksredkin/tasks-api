photo_cache = {}

def get_photo_id(key: str) -> str | None:
    return photo_cache.get(key)

def set_photo_id(key: str, file_id: str) -> None:
    photo_cache[key] = file_id