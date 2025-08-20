import json
from pathlib import Path


def chrome_json_to_html(data: dict) -> str:
    """Convert Chrome's bookmark JSON into a simple HTML bookmark file."""
    header = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\">",
        "<TITLE>Bookmarks</TITLE>",
        "<H1>Bookmarks</H1>",
        "<DL><p>",
    ]

    lines = []

    def walk(node, indent=1):
        pad = "    " * indent
        if node.get("type") == "folder":
            lines.append(f"{pad}<DT><H3>{node.get('name', '')}</H3>")
            lines.append(f"{pad}<DL><p>")
            for child in node.get("children", []):
                walk(child, indent + 1)
            lines.append(f"{pad}</DL><p>")
        elif node.get("type") == "url":
            href = node.get("url", "")
            name = node.get("name", href)
            lines.append(f"{pad}<DT><A HREF=\"{href}\">{name}</A>")

    roots = data.get("roots", {})
    for root in roots.values():
        walk(root)

    footer = ["</DL><p>"]
    return "\n".join(header + lines + footer)


def load_chrome_bookmark_json(path: Path) -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)
