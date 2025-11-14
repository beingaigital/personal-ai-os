from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import List
import json


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"


def _get_monday(date_obj: datetime) -> datetime:
    # Monday is 0
    return date_obj - timedelta(days=date_obj.weekday())


def create_week_folder(target_date: datetime | None = None) -> Path:
    if target_date is None:
        target_date = datetime.now()
    monday = _get_monday(target_date)
    folder_name = monday.strftime("%Y-%m-%d")
    path = RAW_DIR / folder_name
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_current_week_folder() -> Path:
    return create_week_folder(datetime.now())


def list_raw_folders() -> List[Path]:
    if not RAW_DIR.exists():
        return []
    return sorted([p for p in RAW_DIR.iterdir() if p.is_dir()])


def ensure_data_dirs() -> None:
    (DATA_DIR / "medium-rare").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "topic").mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_data_dirs()
    week = get_current_week_folder()
    print(json.dumps({"current_week": str(week)}, ensure_ascii=False))


