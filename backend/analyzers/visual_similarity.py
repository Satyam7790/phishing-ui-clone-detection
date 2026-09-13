from pathlib import Path

def compare_screenshots(first: Path | None, second: Path | None) -> float | None:
    if not first or not second: return None
    try:
        from PIL import Image
        import numpy as np
        a = np.asarray(Image.open(first).convert("L").resize((128, 72)), dtype=float)
        b = np.asarray(Image.open(second).convert("L").resize((128, 72)), dtype=float)
        return round(float(max(0, 1 - np.mean(np.abs(a - b)) / 255)), 4)
    except Exception:
        return None
