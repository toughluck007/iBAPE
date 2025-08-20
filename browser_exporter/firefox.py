import configparser
import os
import shutil
import sqlite3
from pathlib import Path
from typing import Dict, Optional


def _profiles_root() -> Path:
    system = os.sys.platform
    home = Path.home()
    if system.startswith("win"):
        return Path(os.environ.get("APPDATA", home / "AppData/Roaming")) / "Mozilla/Firefox"
    if system == "darwin":
        return home / "Library/Application Support/Firefox"
    return home / ".mozilla/firefox"


def _parse_profiles() -> Dict[str, Path]:
    root = _profiles_root()
    ini = root / "profiles.ini"
    cfg = configparser.ConfigParser()
    profiles: Dict[str, Path] = {}
    if ini.exists():
        cfg.read(ini)
        for section in cfg.sections():
            if section.startswith("Profile"):
                name = cfg.get(section, "Name", fallback=None)
                path = cfg.get(section, "Path", fallback=None)
                if name and path:
                    profiles[name] = root / path
    return profiles


def _default_profile() -> Path:
    profiles = _parse_profiles()
    if not profiles:
        raise FileNotFoundError("No Firefox profiles found")
    # Pick first profile
    return next(iter(profiles.values()))


def export_bookmarks(output_dir: Path, profile: Optional[str] = None) -> Path:
    profiles = _parse_profiles()
    src_dir = profiles.get(profile) if profile else _default_profile()
    places = Path(src_dir) / "places.sqlite"
    if not places.exists():
        raise FileNotFoundError(f"places.sqlite not found in {src_dir}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    dst_native = output_dir / "firefox_places.sqlite"
    shutil.copy2(places, dst_native)

    # Extract basic bookmarks (without hierarchy)
    con = sqlite3.connect(dst_native)
    cur = con.cursor()
    cur.execute(
        """
        SELECT moz_places.url, moz_bookmarks.title
        FROM moz_bookmarks
        JOIN moz_places ON moz_bookmarks.fk = moz_places.id
        WHERE moz_bookmarks.type = 1 AND moz_places.url NOT NULL
        ORDER BY moz_bookmarks.dateAdded
        """
    )
    rows = cur.fetchall()
    con.close()

    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">",
        "<TITLE>Bookmarks</TITLE>",
        "<H1>Bookmarks</H1>",
        "<DL><p>",
    ]
    for url, title in rows:
        name = title or url
        lines.append(f"    <DT><A HREF=\"{url}\">{name}</A>")
    lines.append("</DL><p>")
    dst_html = output_dir / "firefox_bookmarks.html"
    dst_html.write_text("\n".join(lines), encoding="utf-8")
    return dst_html
