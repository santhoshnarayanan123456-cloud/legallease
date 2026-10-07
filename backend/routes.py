from fastapi import APIRouter, HTTPException

from ai_core.gemini_generator import (
    GeminiDocumentGenerator
)

from backend.models import (
    DocumentRequest,
    DocumentResponse
)


router = APIRouter()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):

    try:

        generator = GeminiDocumentGenerator()

        document = generator.generate_document(

            document_type=request.document_type,

            parties=request.parties,

            terms=request.terms,

            dates=request.dates
        )

        return DocumentResponse(
            document=document
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}"
        )