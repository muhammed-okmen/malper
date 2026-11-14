#!/usr/bin/env python3
"""pdf/ peldankasındaki PDF'lerden articles.js dosyasını üretir.

Kullanım:   python3 build.py
Gereken:    pip install pypdf

Bilgiler PDF'in kendi metadata'sından okunur. LaTeX'te preamble'a şunu ekleyin:

  \\usepackage[unicode,
    pdftitle={Sernavê gotarê},
    pdfauthor={Navê te},
    pdfsubject={Kurteya gotarê, du-sê hevok},
    pdfkeywords={Matematîk, Teorî}]{hyperref}

Tarih: PDF'in oluşturulma tarihi. Elle vermek isterseniz pdf/gotar.pdf yanına
pdf/gotar.json koyun: {"date": "2026-11-14", "title": "...", "tags": ["..."]}
(JSON'daki alanlar PDF metadata'sının üstüne yazar.)
"""
import json, re, sys
from datetime import date
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf kurulu değil:  pip install pypdf")

ROOT = Path(__file__).parent
PDF_DIR = ROOT / "pdf"


def parse_date(raw, fallback):
    # PDF tarihi: D:20261114011800+03'00'
    m = re.match(r"D:(\d{4})(\d{2})(\d{2})", raw or "")
    if m:
        return f"{m[1]}-{m[2]}-{m[3]}"
    return fallback


def main():
    if not PDF_DIR.is_dir():
        sys.exit("pdf/ klasörü yok. Oluşturup PDF'lerinizi içine koyun.")
    articles = []
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        info = PdfReader(str(pdf)).metadata or {}
        mtime = date.fromtimestamp(pdf.stat().st_mtime).isoformat()
        tags = [t.strip() for t in re.split(r"[,;]", info.get("/Keywords", "") or "") if t.strip()]
        art = {
            "title": (info.get("/Title") or pdf.stem.replace("-", " ").replace("_", " ")).strip(),
            "author": (info.get("/Author") or "").strip(),
            "date": parse_date(info.get("/CreationDate"), mtime),
            "tags": tags or ["Gotar"],
            "abstract": (info.get("/Subject") or "").strip(),
            "file": f"pdf/{pdf.name}",
        }
        side = pdf.with_suffix(".json")
        if side.exists():
            art.update(json.loads(side.read_text(encoding="utf-8")))
        articles.append(art)
        print("+", art["date"], art["title"])
    out = "window.GOTAR = " + json.dumps(articles, ensure_ascii=False, indent=2) + ";\n"
    (ROOT / "articles.js").write_text(out, encoding="utf-8")
    print(f"\n{len(articles)} gotar → articles.js")


if __name__ == "__main__":
    main()
