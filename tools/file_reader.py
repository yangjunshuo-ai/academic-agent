from pathlib import Path

from docx import Document
from pypdf import PdfReader


def read_file(file_path: str) -> str:
    """
    根据文件后缀读取文件内容。

    当前支持：
    - .pdf
    - .docx
    - .txt
    - .md
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        return read_pdf(path)

    if suffix == ".docx":
        return read_docx(path)

    if suffix in [".txt", ".md"]:
        return path.read_text(encoding="utf-8", errors="ignore")

    raise ValueError(f"暂不支持这种文件类型：{suffix}")


def read_pdf(path: Path) -> str:
    """
    读取 PDF 文本内容。

    注意：
    如果 PDF 是扫描图片，pypdf 可能无法提取正文。
    """
    reader = PdfReader(str(path))
    pages = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"\n\n===== 第 {index} 页 =====\n{text}")

    return "\n".join(pages)


def read_docx(path: Path) -> str:
    """
    读取 Word 文档中的段落文本。
    """
    document = Document(str(path))
    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs)
