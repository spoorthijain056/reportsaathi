
from pathlib import Path
from io import BytesIO
import logging
import traceback

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader
from pypdf.errors import PdfReadError, FileNotDecryptedError

from .db import get_database_value


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_PDF_PAGES = 20

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ReportSaathi")


# --------------------------------------------------
# INITIALIZE FASTAPI
# --------------------------------------------------

app = FastAPI(
    title="ReportSaathi",
    description="Medical report understanding application",
    version="1.0.0",
)


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "application": "ReportSaathi",
        "value": get_database_value(),
    }


# --------------------------------------------------
# API INFORMATION
# --------------------------------------------------

@app.get("/api")
async def api_info():
    return {
        "message": "Welcome to ReportSaathi",
        "application": "ReportSaathi",
        "documentation": "/docs",
        "health": "/api/health",
        "analyze": "/api/analyze",
    }


# --------------------------------------------------
# PDF REPORT UPLOAD AND TEXT EXTRACTION
# --------------------------------------------------

@app.post("/api/analyze")
async def analyze_report(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a PDF file."
        )

    filename = Path(file.filename).name

    if Path(filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported currently."
        )

    try:
        # Read uploaded file with size limit
        content = await file.read(MAX_FILE_SIZE + 1)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF size must not exceed 10 MB."
            )

        # Check PDF file signature
        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file does not appear to be a valid PDF."
            )

        # Read PDF
        reader = PdfReader(BytesIO(content), strict=False)

        if reader.is_encrypted:
            try:
                decrypted = reader.decrypt("")
            except Exception:
                decrypted = 0

            if not decrypted:
                raise HTTPException(
                    status_code=400,
                    detail="Password-protected PDFs are not supported."
                )

        # Check number of pages
        if len(reader.pages) > MAX_PDF_PAGES:
            raise HTTPException(
                status_code=400,
                detail="PDF cannot contain more than 20 pages."
            )

        # Extract text from all pages
        extracted_pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""

            extracted_pages.append(
                f"Page {page_number}:\n{page_text}"
            )

        extracted_text = "\n\n".join(extracted_pages).strip()

        # Check extracted text
        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail=(
                    "No readable text found. This may be a scanned PDF. "
                    "OCR support is required to process it."
                )
            )

        logger.info("Successfully processed PDF: %s", filename)

        return {
            "success": True,
            "filename": filename,
            "total_pages": len(reader.pages),
            "extracted_text": extracted_text,
            "message": "PDF uploaded and text extracted successfully.",
            "safety_notice": (
                "Automatically extracted information may contain errors. "
                "Verify all values against the original medical report. "
                "This application does not provide a diagnosis."
            )
        }

    except HTTPException:
        raise

    except FileNotDecryptedError:
        raise HTTPException(
            status_code=400,
            detail="This PDF is encrypted and cannot be read."
        )

    except PdfReadError as error:
        logger.exception("PDF reading error")

        raise HTTPException(
            status_code=400,
            detail=f"PDF reading failed: {str(error)}"
        )

    except Exception as error:
        logger.exception("Unexpected PDF processing error")

        # Detailed error is useful during local development.
        raise HTTPException(
            status_code=500,
            detail=f"PDF processing failed: {str(error)}"
        )

    finally:
        await file.close()


# --------------------------------------------------
# SERVE FRONTEND
# --------------------------------------------------

STATIC_DIR = Path(__file__).resolve().parent / "static"

if (STATIC_DIR / "index.html").is_file():
    app.mount(
        "/",
        StaticFiles(
            directory=str(STATIC_DIR),
            html=True
        ),
        name="static"
    )
