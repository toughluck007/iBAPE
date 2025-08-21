import os
import shutil
from pathlib import Path
from typing import Optional

from .utils import chrome_json_to_html, load_chrome_bookmark_json


def _default_chrome_path(profile: str = "Default") -> Path:
    system = os.sys.platform
    home = Path.home()
    if system.startswith("win"):
        base = Path(os.environ.get("LOCALAPPDATA", home / "AppData/Local"))
        return base / "Google/Chrome/User Data" / profile / "Bookmarks"
    if system == "darwin":
        return home / "Library/Application Support/Google/Chrome" / profile / "Bookmarks"
    # Assume Linux
    return home / ".config/google-chrome" / profile / "Bookmarks"


def export_bookmarks(output_dir: Path, profile: str = "Default") -> Path:
    """Export Chrome bookmarks to output_dir. Returns path to HTML file."""
    src = _default_chrome_path(profile)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        raise FileNotFoundError(f"Chrome bookmarks not found at {src}")

    dst_native = output_dir / "chrome_bookmarks.json"
    shutil.copy2(src, dst_native)

    data = load_chrome_bookmark_json(dst_native)
    html = chrome_json_to_html(data)
    dst_html = output_dir / "chrome_bookmarks.html"
    dst_html.write_text(html, encoding="utf-8")
    return dst_html
