from google import genai

from backend.config import get_settings


class GeminiDocumentGenerator:
    """
    Generates legal-document drafts using Google Gemini.
    """

    def __init__(self):

        settings = get_settings()

        api_key = (settings.gemini_api_key or "").strip()
        model = (settings.gemini_model or "gemini-2.5-flash").strip()

        if not api_key:

            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Create a .env file and add your Gemini API key."
            )

        if model.startswith("models/"):
            model = model.removeprefix("models/")

        if model == "gemini-3.5-flash":
            model = "gemini-2.5-flash"

        self.model = model

        self.client = genai.Client(
            api_key=api_key
        )

    @staticmethod
    def convert_terms_to_bullets(terms):

        normalized_terms = (terms or "").strip()

        parts = [
            item.strip()
            for item in normalized_terms.split(";")
            if item.strip()
        ]

        if not parts:

            return f"- {normalized_terms}" if normalized_terms else "- "

        return "\n".join(
            f"- {item}"
            for item in parts
        )

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        terms_bullets = self.convert_terms_to_bullets(
            terms
        )

        prompt = f"""
You are LegalEase, an AI-powered legal document
drafting assistant.

Create a professional DRAFT of a:

{document_type}

USER INFORMATION

Document Type:
{document_type}

Parties:
{parties}

Effective Date:
{dates}

Requested Terms:
{terms_bullets}


IMPORTANT INSTRUCTIONS

1. Create a complete editable legal-document draft.

2. Use only information supplied by the user.

3. Never invent:
- names
- addresses
- dates
- payment amounts
- laws
- statutes
- court cases
- registration numbers
- legal facts

4. If important information is missing,
use a placeholder such as:

[INSERT ADDRESS]

or

[INSERT AMOUNT]

5. Use professional legal-document structure.

6. Include:
- title
- introductory section
- parties
- purpose
- definitions where appropriate
- numbered clauses
- terms and conditions
- termination where appropriate
- confidentiality where appropriate
- signatures

7. Preserve the user's requested terms.

8. Do not claim that this document is guaranteed
to be legally valid or enforceable.

9. Do not provide a legal opinion.

10. End with a short section called:

DRAFTING NOTE

The drafting note should tell the user that
the document should be reviewed by a qualified
legal professional for the applicable jurisdiction
before signing.

11. Return plain text.

12. Do not use Markdown code fences.

Generate the document now.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        text = getattr(
            response,
            "text",
            None
        )

        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()