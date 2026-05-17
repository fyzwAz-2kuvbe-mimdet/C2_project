import io

import pypdf
from docx import Document


def load_text_from_file(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    if name.endswith(".pdf"):
        return _load_pdf(uploaded_file)
    if name.endswith(".docx"):
        return _load_docx(uploaded_file)
    if name.endswith(".txt"):
        return _load_txt(uploaded_file)
    raise ValueError(f"지원하지 않는 파일 형식입니다: {name}")


def _load_pdf(file) -> str:
    reader = pypdf.PdfReader(io.BytesIO(file.read()))
    return "\n".join(
        page.extract_text() for page in reader.pages if page.extract_text()
    )


def _load_docx(file) -> str:
    doc = Document(io.BytesIO(file.read()))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def _load_txt(file) -> str:
    raw = file.read()
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")
