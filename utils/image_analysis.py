def analyze_rooftop(image):
    # Estimate rooftop area based on image dimensions (simplified logic)
    height, width, _ = image.shape
    total_area = (height * width) / 10000  # basic conversion to m^2
    usable_area = total_area * 0.6  # assume 60% is usable

    return {
        "total_area_m2": round(total_area, 2),
        "usable_area_m2": round(usable_area, 2),
        "obstacles": "Estimated heuristically"
    }
