from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
import json


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"


def _get_monday(date_obj: datetime) -> datetime:
    """
    获取指定日期所在周的周一日期
    
    Args:
        date_obj: 目标日期
        
    Returns:
        周一日期（datetime对象）
    """
    # Monday is 0 in weekday()
    return date_obj - timedelta(days=date_obj.weekday())


def get_week_monday(target_date: Optional[datetime] = None) -> datetime:
    """
    获取指定日期所在周的周一
    
    Args:
        target_date: 目标日期，如果为None则使用当前日期
        
    Returns:
        周一日期（datetime对象）
    """
    if target_date is None:
        target_date = datetime.now()
    return _get_monday(target_date)


def create_week_folder(target_date: Optional[datetime] = None, auto_create: bool = True) -> Path:
    """
    创建或获取当前周（以周一为基准）的文件夹
    
    Args:
        target_date: 目标日期，如果为None则使用当前日期
        auto_create: 是否自动创建文件夹（如果不存在）
        
    Returns:
        周文件夹路径（如 data/raw/2025-01-13/）
    """
    if target_date is None:
        target_date = datetime.now()
    monday = _get_monday(target_date)
    folder_name = monday.strftime("%Y-%m-%d")
    path = RAW_DIR / folder_name
    
    if auto_create:
        path.mkdir(parents=True, exist_ok=True)
    
    return path


def get_current_week_folder(auto_create: bool = True) -> Path:
    """
    获取当前周（以周一为基准）的文件夹
    
    Args:
        auto_create: 是否自动创建文件夹（如果不存在）
        
    Returns:
        当前周的文件夹路径
    """
    return create_week_folder(datetime.now(), auto_create=auto_create)


def get_week_folder_info(target_date: Optional[datetime] = None) -> dict:
    """
    获取周文件夹的详细信息
    
    Args:
        target_date: 目标日期，如果为None则使用当前日期
        
    Returns:
        包含周信息的字典
    """
    if target_date is None:
        target_date = datetime.now()
    
    monday = _get_monday(target_date)
    sunday = monday + timedelta(days=6)
    folder_path = RAW_DIR / monday.strftime("%Y-%m-%d")
    
    # 检查文件夹是否存在，统计文件数量
    file_count = 0
    if folder_path.exists():
        file_count = len([
            f for f in folder_path.iterdir()
            if f.is_file() and f.suffix.lower() in {".md", ".markdown", ".txt", ".pdf", ".docx"}
        ])
    
    return {
        "week_monday": monday.strftime("%Y-%m-%d"),
        "week_sunday": sunday.strftime("%Y-%m-%d"),
        "folder_path": str(folder_path),
        "folder_exists": folder_path.exists(),
        "file_count": file_count,
        "week_range": f"{monday.strftime('%Y-%m-%d')} ~ {sunday.strftime('%Y-%m-%d')}",
    }


def list_raw_folders() -> List[Path]:
    """
    列出所有raw目录下的周文件夹
    
    Returns:
        周文件夹路径列表（按日期排序）
    """
    if not RAW_DIR.exists():
        return []
    return sorted([p for p in RAW_DIR.iterdir() if p.is_dir() and p.name.count("-") == 2])


def ensure_data_dirs() -> None:
    """
    确保必要的目录结构存在
    """
    (DATA_DIR / "medium-rare").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "topic").mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_data_dirs()
    week = get_current_week_folder()
    print(json.dumps({"current_week": str(week)}, ensure_ascii=False))


