from docx import Document
import PyPDF2
import io


def extract_text_from_file(file_content, filename):
    """
    Extract text from uploaded file

    Supports: .txt, .pdf, .docx
    """

    file_extension = filename.lower().split(".")[-1]

    try:
        if file_extension == "txt":
            return extract_from_txt(file_content)
        elif file_extension == "pdf":
            return extract_from_pdf(file_content)
        elif file_extension in ["docx", "doc"]:
            return extract_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    except Exception as e:
        raise Exception(f"Error processing file: {str(e)}")


def extract_from_txt(file_content):
    """Extract text from TXT file"""
    try:
        return file_content.decode("utf-8")
    except UnicodeDecodeError:
        return file_content.decode("latin-1")


def extract_from_pdf(file_content):
    """Extract text from PDF file"""
    pdf_file = io.BytesIO(file_content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"

    return text.strip()


def extract_from_docx(file_content):
    """Extract text from DOCX file"""
    docx_file = io.BytesIO(file_content)
    doc = Document(docx_file)

    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text.strip()


def process_multiple_documents(files_data):
    """
    Process multiple documents and return combined results

    files_data: list of dicts with 'content' and 'filename'
    """
    results = []

    for file_data in files_data:
        try:
            text = extract_text_from_file(file_data["content"], file_data["filename"])

            results.append(
                {
                    "filename": file_data["filename"],
                    "text": text,
                    "status": "success",
                    "length": len(text),
                }
            )
        except Exception as e:
            results.append(
                {"filename": file_data["filename"], "status": "error", "error": str(e)}
            )

    return results
