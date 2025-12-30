from PIL import Image
import io


def validate_image(image_bytes: bytes) -> dict:
    image = Image.open(io.BytesIO(image_bytes))
    dpi = image.info.get("dpi", (72, 72))[0]

    issues = []
    if dpi < 300:
        issues.append({
            "issue": f"Low resolution artwork ({dpi} DPI)",
            "severity": "high"
        })

    return {
        "width_px": image.width,
        "height_px": image.height,
        "dpi": dpi,
        "issues": issues
    }