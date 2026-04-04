#!/usr/bin/env python3
"""
PDF to text extractor for paper-reader skill.

Usage:
    python3 pdf_to_txt.py paper1.pdf paper2.pdf ...

Output:
    Creates <filename>.txt next to each PDF.
    Prints the path of each output file on success.

Requirements:
    pip install PyPDF2
    (or: pip install pypdf  — the maintained fork, same API)
"""

import sys
import os

def extract(pdf_path: str) -> str:
    """Return the path to the extracted .txt file."""
    try:
        import PyPDF2
    except ImportError:
        try:
            import pypdf as PyPDF2  # newer maintained fork
        except ImportError:
            print("ERROR: PyPDF2 not installed. Run: pip install PyPDF2", file=sys.stderr)
            sys.exit(1)

    text_parts = []
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
    except Exception as e:
        print(f"ERROR reading {pdf_path}: {e}", file=sys.stderr)
        return ""

    out_path = pdf_path + ".txt"
    with open(out_path, "w", encoding="utf-8", errors="ignore") as out:
        out.write("\n\n".join(text_parts))

    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pdf_to_txt.py file1.pdf [file2.pdf ...]")
        sys.exit(1)

    for pdf in sys.argv[1:]:
        result = extract(pdf)
        if result:
            size_kb = os.path.getsize(result) // 1024
            print(f"OK  {result}  ({size_kb} KB)")
        else:
            print(f"FAIL  {pdf}")
