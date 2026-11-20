#!/usr/bin/env python3
"""CAAVE Trinity Path novel swarm: resumable, canon-grounded chapter drafting.
Requires user-supplied canon JSON and an explicitly configured compatible LLM endpoint.
Outputs are drafts, not finished 600-page books. No publishing or minting.
"""
import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from docx import Document

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config"
OUTPUT = ROOT / "output" / "caave_empire"
NOVELS = OUTPUT / "novels"
BLACKBOARD = OUTPUT / "blackboard.json"

SYSTEM = """You are the Trinity Path of Ma'at novel drafting assistant.
Respect the supplied series, character and power-system canon. Do not invent
named 144-strikes or established facts absent from canon. Write original,
cinematic, action-forward prose with emotional stakes, martial philosophy,
Fear → Power → Peace development and a meaningful lesson. Never claim a
draft is a completed manuscript. Avoid filling space with repetition."""

def read_json(name):
    path = CONFIG / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing {path}. Supply approved canon first.")
    return json.loads(path.read_text(encoding="utf-8"))

def load_canon():
    series = read_json("series.json")
    chars = read_json("character_bible.json")
    powers = read_json("power_system.json")
    books = series.get("books")
    if not isinstance(books, list) or len(books) != 25:
        raise ValueError("series.json must have exactly 25 books")
    ids = [b.get("id") for b in books]
    if sorted(ids) != list(range(1,26)):
        raise ValueError("Book ids must be unique integers 1..25")
    return books, chars, powers

def llm(prompt):
    url = os.getenv("CAAVE_LLM_API_URL", "").strip()
    key = os.getenv("CAAVE_LLM_API_KEY", "").strip()
    model = os.getenv("CAAVE_LLM_MODEL", "").strip()
    if not (url and key and model):
        raise RuntimeError("Set CAAVE_LLM_API_URL, CAAVE_LLM_API_KEY, CAAVE_LLM_MODEL")
    if not url.startswith("https://"):
        raise ValueError("LLM API URL must use HTTPS")
    response = requests.post(url, headers={"Authorization":f"Bearer {key}"},
        json={"model":model,"messages":[{"role":"system","content":SYSTEM},
            {"role":"user","content":prompt}],"max_tokens":6000},
        timeout=180)
    response.raise_for_status()
    data = response.json()
    result = data["choices"][0]["message"]["content"]
    if not isinstance(result,str) or len(result.strip()) < 200:
        raise ValueError("LLM returned insufficient prose; nothing saved")
    return result.strip()

def save_docx(book, chapters, dest):
    doc = Document()
    doc.add_heading(book["title"], 0)
    doc.add_paragraph("Trinity Path of Ma'at — draft manuscript")
    doc.add_paragraph("Beverly & Sons Marketing and Consulting LLC | CAAVE-2026-001")
    for number, prose in enumerate(chapters, 1):
        doc.add_heading(f"Chapter {number}", level=1)
        for paragraph in re.split(r"\n\s*\n", prose):
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())
    doc.save(dest)

def generate(book, chars, powers, chapter_count, dry_run=False):
    book_id = book["id"]
    book_dir = NOVELS / f"book_{book_id:02d}_chapters"
    book_dir.mkdir(parents=True, exist_ok=True)
    previous = ""
    chapters = []
    for chapter_num in range(1, chapter_count+1):
        path = book_dir / f"chapter_{chapter_num:02d}.txt"
        if path.exists():
            prose = path.read_text(encoding="utf-8")
        else:
            prompt = json.dumps({
                "book":book,"chapter":chapter_num,"total_planned_chapters":chapter_count,
                "character_bible":chars,"power_system":powers,
                "previous_chapter_tail":previous[-3000:],
                "instructions":"Write this chapter as substantive continuous prose. Advance the plot; maintain continuity. End with a one-line lesson. Return prose only."
            },ensure_ascii=False)
            if dry_run:
                print(f"DRY RUN book {book_id} chapter {chapter_num}: prompt ready ({len(prompt)} chars)")
                continue
            prose = llm(prompt)
            path.write_text(prose,encoding="utf-8")
        chapters.append(prose)
        previous = prose
    if dry_run:
        return
    dest = NOVELS / f"book_{book_id:02d}.docx"
    save_docx(book,chapters,dest)
    board = json.loads(BLACKBOARD.read_text(encoding="utf-8")) if BLACKBOARD.exists() else {}
    registry = board.setdefault("content_registry",[])
    registry = [x for x in registry if x.get("id") != book_id or x.get("type") != "book"]
    registry.append({"type":"book","id":book_id,"title":book["title"],
        "path":str(dest.relative_to(ROOT)),"status":"draft_needs_editorial_review",
        "chapters_drafted":len(chapters),
        "nft_metadata":{"title":book["title"],"status":"not_minted"},
        "kdp_metadata":{"title":book["title"],"status":"not_published"},
        "shorts_metadata":{"source_book":book_id,"status":"not_published"}})
    board["content_registry"] = registry
    board["swarm_status"] = "drafting"
    board["updated_at"] = datetime.now(timezone.utc).isoformat()
    BLACKBOARD.write_text(json.dumps(board,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"Saved draft: {dest}")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--book",type=int,choices=range(1,26),metavar="1..25",
                        help="Book to draft; default all 25")
    parser.add_argument("--chapters",type=int,default=24)
    parser.add_argument("--dry-run",action="store_true")
    args=parser.parse_args()
    if not 1 <= args.chapters <= 60:
        parser.error("--chapters must be 1..60")
    books,chars,powers=load_canon()
    OUTPUT.mkdir(parents=True,exist_ok=True)
    NOVELS.mkdir(parents=True,exist_ok=True)
    for book in books:
        if args.book is None or args.book == book["id"]:
            generate(book,chars,powers,args.chapters,args.dry_run)

if __name__=="__main__":
    main()
