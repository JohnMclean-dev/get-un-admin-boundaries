import os

def get_filename_from_url(url: str) -> str:
    return os.path.basename(url)

def should_skip_file(path: str, skip_existing: bool) -> bool:
    return skip_existing and os.path.exists(path)