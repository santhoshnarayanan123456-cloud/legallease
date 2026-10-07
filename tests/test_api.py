from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["name"] == "LegalEase"


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


def test_generate_validation():

    response = client.post(

        "/generate",

        json={

            "document_type": "",

            "parties": "A",

            "terms": "B",

            "dates": "C"
        }
    )


    assert response.status_code == 422


def test_generate_with_mock(
    monkeypatch
):

    class FakeGenerator:

        def __init__(self):
            pass


        def generate_document(
            self,
            **kwargs
        ):

            assert (
                kwargs["document_type"]
                == "NDA"
            )


            return (
                "NDA DRAFT\n\n"
                "1. Confidentiality\n"
                "- Keep information confidential."
            )


    monkeypatch.setattr(

        "backend.routes.GeminiDocumentGenerator",

        FakeGenerator
    )


    response = client.post(

        "/generate",

        json={

            "document_type":
                "NDA",

            "parties":
                "Alice (Disclosing), "
                "Bob (Receiving)",

            "terms":
                "Confidentiality must be maintained",

            "dates":
                "October 5, 2026"
        }
    )


    assert response.status_code == 200

    assert (
        "NDA DRAFT"
        in response.json()["document"]
    )