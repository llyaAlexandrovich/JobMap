import re

def dms_to_dd(dms_str) -> float | None:
    match = re.search(r"(\d+)°\s*(\d+)'\s*([\d.]+)\"\s*([NSEW])", dms_str)
    
    if not match:
        return
        
    degrees = float(match.group(1))
    minutes = float(match.group(2))
    seconds = float(match.group(3))
    direction = match.group(4)

    dd = degrees + (minutes / 60) + (seconds / 3600)

    if direction in ['S', 'W']:
        dd = -dd

    return round(dd, 6)


def normalize_coords(dms_str: str) -> tuple[float, float] | None:
    coords = dms_str.split(' ') # lat | lon
    lat = dms_to_dd(coords[0])
    lon = dms_to_dd(coords[0])
    return None if lat is None or lon is None else (lat, lon)
