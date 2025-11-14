from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from .folder_manager import ensure_data_dirs
from .kimi_client import load_kimi_client


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
MEDIUM_RARE_DIR = DATA_DIR / "medium-rare"
CONFIG_DIR = ROOT / "config"

SUPPORTED_TEXT_EXTS = {".md", ".markdown", ".txt"}
SUPPORTED_DOCUMENT_EXTS = SUPPORTED_TEXT_EXTS | {".pdf", ".docx"}


def _extract_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError as exc:
        raise RuntimeError("缺少依赖 pypdf，请先安装：pip install pypdf") from exc
    reader = PdfReader(str(path))
    texts: List[str] = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts).strip()


def _extract_docx(path: Path) -> str:
    try:
        from docx import Document  # type: ignore
    except ImportError as exc:
        raise RuntimeError("缺少依赖 python-docx，请先安装：pip install python-docx") from exc
    document = Document(str(path))
    return "\n".join(para.text for para in document.paragraphs).strip()


def extract_text_from_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in SUPPORTED_TEXT_EXTS:
        return _extract_text_file(path)
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix == ".docx":
        return _extract_docx(path)
    raise ValueError(f"Unsupported file extension: {path.suffix}")


def read_documents(folder: Path) -> List[Dict[str, str]]:
    candidates = sorted(
        [
            p
            for p in folder.iterdir()
            if p.is_file() and p.suffix.lower() in SUPPORTED_DOCUMENT_EXTS
        ]
    )
    if not candidates:
        return []

    def load(index_path: Tuple[int, Path]) -> Tuple[int, Dict[str, str]]:
        idx, file_path = index_path
        text = extract_text_from_file(file_path)
        return idx, {"name": file_path.name, "content": text}

    max_workers = min(8, len(candidates))
    results: List[Tuple[int, Dict[str, str]]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(load, (idx, path)) for idx, path in enumerate(candidates)
        ]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda item: item[0])
    return [item[1] for item in results]


def build_summary_prompt(files: List[Dict[str, str]]) -> str:
    parts = [
        "You are an assistant that summarizes multiple Markdown notes.",
        "For each file, produce:",
        "1) Summary (concise)",
        "2) Key Takeaways (bullet points)",
        "3) Something New (non-obvious insights)",
        "",
        "Format:",
        "### <filename>",
        "Summary: ...",
        "Key Takeaways:",
        "- ...",
        "- ...",
        "Something New: ...",
        "",
    ]
    for f in files:
        parts.append(f"---\n# File: {f['name']}\n{f['content']}\n")
    return "\n".join(parts)


def write_summary_output(week_folder: Path, output_text: str) -> Path:
    out_name = f"{week_folder.name}.md"
    out_path = MEDIUM_RARE_DIR / out_name
    out_path.write_text(output_text, encoding="utf-8")
    return out_path


def summarize_week(week_folder: Path) -> Path:
    ensure_data_dirs()
    files = read_documents(week_folder)
    if not files:
        raise RuntimeError(f"No supported documents found in {week_folder}")
    prompt = build_summary_prompt(files)
    # 信息提炼功能使用 kimi-latest 模型
    kimi = load_kimi_client(str(CONFIG_DIR / "kimi_api.json"), model_override="kimi-latest")
    messages = [
        {"role": "system", "content": "Summarize and analyze the given materials with accuracy and clarity."},
        {"role": "user", "content": prompt},
    ]
    output = kimi.chat_completion(messages)
    return write_summary_output(week_folder, output)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Summarize weekly raw markdowns into a Medium-Rare document.")
    parser.add_argument("--week", type=str, required=True, help="Path to the weekly folder under data/raw/YYYY-MM-DD")
    args = parser.parse_args()
    week_path = Path(args.week).expanduser().resolve()
    result = summarize_week(week_path)
    print(json.dumps({"output": str(result)}, ensure_ascii=False))


