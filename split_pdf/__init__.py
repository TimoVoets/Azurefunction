import azure.functions as func
import tempfile
import PyPDF2

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get("file")
        page_number_str = req.form.get("page_number")

        if not file or not page_number_str:
            return func.HttpResponse("Missing file or page_number", status_code=400)

        page_number = int(page_number_str)
        if page_number < 1:
            return func.HttpResponse("Page number must be >= 1", status_code=400)

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = f"{tmpdir}/input.pdf"
            file.save(input_path)

            reader = PyPDF2.PdfReader(input_path)
            if page_number > len(reader.pages):
                return func.HttpResponse("Page number out of range", status_code=400)

            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[page_number - 1])

            output_path = f"{tmpdir}/page_{page_number}.pdf"
            with open(output_path, "wb") as f_out:
                writer.write(f_out)

            with open(output_path, "rb") as f:
                return func.HttpResponse(
                    f.read(),
                    mimetype="application/pdf",
                    headers={
                        "Content-Disposition": f"attachment; filename=page_{page_number}.pdf"
                    }
                )

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
