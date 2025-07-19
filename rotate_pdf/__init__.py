from fastapi import APIRouter, UploadFile, File, Response
import tempfile
import os
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract

router = APIRouter()

def detect_rotation_angle(image: Image.Image) -> int:
    try:
        osd = pytesseract.image_to_osd(image)
        for line in osd.splitlines():
            if "Rotate" in line:
                return int(line.split(":")[1].strip())
    except Exception as e:
        print("Fout bij rotatiedetectie:", e)
    return 0

def correct_image_rotation(pil_image: Image.Image, angle: int) -> Image.Image:
    if angle == 90:
        return pil_image.rotate(-90, expand=True)
    elif angle == 180:
        return pil_image.rotate(-180, expand=True)
    elif angle == 270:
        return pil_image.rotate(-270, expand=True)
    return pil_image

@router.post("/rotate")
async def rotate_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        images = convert_from_bytes(contents, dpi=300)

        rotated_images = []
        for img in images:
            angle = detect_rotation_angle(img)
            rotated = correct_image_rotation(img, angle)
            rotated_images.append(rotated.convert("RGB"))

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = f"{tmpdir}/rotated_output.pdf"
            rotated_images[0].save(output_path, save_all=True, append_images=rotated_images[1:])
            with open(output_path, "rb") as f:
                pdf_bytes = f.read()

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=rotated_output.pdf"}
        )

    except Exception as e:
        return Response(content=f"Error: {str(e)}", status_code=500)
