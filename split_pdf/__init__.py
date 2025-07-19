from fastapi import APIRouter, UploadFile, File, Form, Response
import tempfile
import PyPDF2

router = APIRouter()

@router.post("/split")
async def split_pdf(file: UploadFile = File(...), page_number: int = Form(...)):
    try:
        # Lees het geüploade bestand in bytes
        contents = await file.read()

        if page_number < 1:
            return Response(content="Page number must be >= 1", status_code=400)

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = f"{tmpdir}/input.pdf"
            with open(input_path, "wb") as f:
                f.write(contents)

            reader = PyPDF2.PdfReader(input_path)
            if page_number > len(reader.pages):
                return Response(content="Page number out of range", status_code=400)

            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[page_number - 1])

            output_path = f"{tmpdir}/page_{page_number}.pdf"
            with open(output_path, "wb") as f_out:
                writer.write(f_out)

            with open(output_path, "rb") as f:
                pdf_bytes = f.read()

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=page_{page_number}.pdf"}
        )

    except Exception as e:
        return Response(content=f"Error: {str(e)}", status_code=500)
