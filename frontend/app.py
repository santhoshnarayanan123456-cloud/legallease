import os
import tempfile

from pathlib import Path

import requests

import streamlit as st

from dotenv import load_dotenv


load_dotenv()


from utils.document_formatter import (
    format_docx,
    format_html_preview,
    format_pdf,
    sanitize_text
)


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(

    page_title="LegalEase",

    page_icon="⚖️",

    layout="wide"
)


# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main-title {

        text-align: center;

        font-size: 2.5rem;

        font-weight: 700;

    }

    .subtitle {

        text-align: center;

        color: #9ca3af;

        margin-bottom: 1.5rem;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# HEADER
# -----------------------------

st.markdown(

    '<div class="main-title">'
    '⚖️ LegalEase'
    '</div>',

    unsafe_allow_html=True
)


st.markdown(

    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',

    unsafe_allow_html=True
)


st.warning(

    "LegalEase creates AI-generated drafts "
    "for informational purposes. Have a "
    "qualified lawyer review important "
    "documents before signing or relying "
    "on them."
)


# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header(
        "Document Settings"
    )


    document_type = st.selectbox(

        "Document Type",

        [

            "Employment Contract",

            "Non-Disclosure Agreement",

            "Lease Agreement",

            "Employment Offer Letter",

            "Service Agreement",

            "Freelance Work Contract",

            "General Agreement"

        ]
    )


    custom_type = st.text_input(

        "Or enter a custom document type"
    )


    if custom_type.strip():

        document_type = custom_type.strip()


    logo = st.file_uploader(

        "Optional Logo",

        type=[
            "png",
            "jpg",
            "jpeg"
        ],

        help=(
            "Logo will be used "
            "in DOCX and PDF exports."
        )
    )


# -----------------------------
# INPUT SECTION
# -----------------------------

col1, col2 = st.columns(2)


with col1:

    parties = st.text_area(

        "Parties Involved",

        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),

        height=130
    )


    dates = st.text_input(

        "Effective Date",

        placeholder="October 5, 2026"
    )


with col2:

    terms = st.text_area(

        "Terms & Conditions",

        placeholder=(
            "Payment to be made within 30 days "
            "of invoice; Confidentiality must be "
            "maintained; Either party may terminate "
            "with 15 days notice"
        ),

        height=190,

        help=(
            "Separate each term using "
            "a semicolon (;)."
        )
    )


# -----------------------------
# GENERATE BUTTON
# -----------------------------

if st.button(

    "✨ Generate Document",

    type="primary",

    use_container_width=True
):

    if not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms and conditions."
        )

    elif not dates.strip():

        st.error(
            "Please enter the effective date."
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "dates":
                dates
        }


        try:

            with st.spinner(
                "Generating your legal document..."
            ):

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=120
                )


            if response.ok:

                data = response.json()

                st.session_state[
                    "document"
                ] = data["document"]

                st.session_state[
                    "editing"
                ] = False

                st.success(
                    "Document generated successfully!"
                )


            else:

                try:

                    detail = response.json().get(
                        "detail",
                        response.text
                    )

                except Exception:

                    detail = response.text


                st.error(

                    f"Backend Error "
                    f"({response.status_code}): "
                    f"{detail}"
                )


        except requests.RequestException as exc:

            st.error(

                "Could not connect to FastAPI.\n\n"

                f"Backend URL: {BACKEND_URL}\n\n"

                f"Error: {exc}"
            )


# -----------------------------
# DOCUMENT AREA
# -----------------------------

document = st.session_state.get(
    "document"
)


if document:

    st.divider()

    st.subheader(
        "Generated Document"
    )


    # EDIT BUTTON

    if st.button(

        "✏️ "
        + (
            "Close Editor"
            if st.session_state.get(
                "editing",
                False
            )
            else
            "Edit Document"
        )
    ):

        st.session_state[
            "editing"
        ] = not st.session_state.get(
            "editing",
            False
        )

        st.rerun()


    # EDITOR

    if st.session_state.get(
        "editing",
        False
    ):

        edited_document = st.text_area(

            "Edit Your Document",

            value=document,

            height=600
        )


        st.session_state[
            "document"
        ] = edited_document


        document = edited_document


    # PREVIEW

    st.markdown(
        "### Preview"
    )


    st.markdown(

        format_html_preview(
            document
        ),

        unsafe_allow_html=True
    )


    # -----------------------------
    # DOWNLOADS
    # -----------------------------

    st.markdown(
        "### Download"
    )


    safe_type = "".join(

        character
        if character.isalnum()
        else "_"

        for character
        in document_type.lower()
    ).strip("_")


    if not safe_type:

        safe_type = "legal_document"


    # Logo temporary file

    logo_path = None


    if logo is not None:

        suffix = (
            Path(
                logo.name
            ).suffix.lower()
            or ".png"
        )


        temp_logo = tempfile.NamedTemporaryFile(

            delete=False,

            suffix=suffix
        )


        temp_logo.write(
            logo.getvalue()
        )


        temp_logo.close()


        logo_path = temp_logo.name


    # TXT

    txt_bytes = sanitize_text(
        document
    ).encode(
        "utf-8"
    )


    # DOCX

    docx_bytes = format_docx(

        document,

        document_type,

        logo_path=logo_path
    )


    # PDF

    pdf_bytes = format_pdf(

        document,

        document_type,

        logo_path=logo_path
    )


    download1, download2, download3 = st.columns(3)


    with download1:

        st.download_button(

            "⬇️ Download TXT",

            data=txt_bytes,

            file_name=(
                f"{safe_type}.txt"
            ),

            mime="text/plain",

            use_container_width=True
        )


    with download2:

        st.download_button(

            "⬇️ Download DOCX",

            data=docx_bytes,

            file_name=(
                f"{safe_type}.docx"
            ),

            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),

            use_container_width=True
        )


    with download3:

        st.download_button(

            "⬇️ Download PDF",

            data=pdf_bytes,

            file_name=(
                f"{safe_type}.pdf"
            ),

            mime="application/pdf",

            use_container_width=True
        )


    # Delete temporary logo

    if logo_path:

        try:

            os.unlink(
                logo_path
            )

        except OSError:

            pass