import argparse
from pathlib import Path

from . import chrome, edge, firefox


BROWSERS = {
    "chrome": chrome.export_bookmarks,
    "edge": edge.export_bookmarks,
    "firefox": firefox.export_bookmarks,
}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export browser bookmarks")
    parser.add_argument("output", type=Path, help="Directory to save exported bookmarks")
    parser.add_argument(
        "--browsers",
        nargs="+",
        choices=BROWSERS.keys(),
        default=list(BROWSERS.keys()),
        help="Browsers to export",
    )
    args = parser.parse_args(argv)

    for name in args.browsers:
        try:
            BROWSERS[name](args.output)
            print(f"Exported {name} bookmarks to {args.output}")
        except FileNotFoundError as exc:
            print(f"{name}: {exc}")


if __name__ == "__main__":
    main()
