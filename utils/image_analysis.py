import numpy as np

def analyze_rooftop(image: np.ndarray):
    height, width, _ = image.shape
    total_area = (height * width) / 10000  # simplistic conversion
    usable_area = total_area * 0.6
    return {
        "total_area_m2": round(total_area, 2),
        "usable_area_m2": round(usable_area, 2),
        "obstacles": "Estimated heuristically"
    }
