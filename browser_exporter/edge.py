import os
import shutil
from pathlib import Path

from .utils import chrome_json_to_html, load_chrome_bookmark_json


def _default_edge_path(profile: str = "Default") -> Path:
    system = os.sys.platform
    home = Path.home()
    if system.startswith("win"):
        base = Path(os.environ.get("LOCALAPPDATA", home / "AppData/Local"))
        return base / "Microsoft/Edge/User Data" / profile / "Bookmarks"
    if system == "darwin":
        return home / "Library/Application Support/Microsoft Edge" / profile / "Bookmarks"
    # Assume Linux
    return home / ".config/microsoft-edge" / profile / "Bookmarks"


def export_bookmarks(output_dir: Path, profile: str = "Default") -> Path:
    src = _default_edge_path(profile)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        raise FileNotFoundError(f"Edge bookmarks not found at {src}")

    dst_native = output_dir / "edge_bookmarks.json"
    shutil.copy2(src, dst_native)

    data = load_chrome_bookmark_json(dst_native)
    html = chrome_json_to_html(data)
    dst_html = output_dir / "edge_bookmarks.html"
    dst_html.write_text(html, encoding="utf-8")
    return dst_html
