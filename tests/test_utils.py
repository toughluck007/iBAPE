from browser_exporter.utils import chrome_json_to_html


def test_chrome_json_to_html_basic():
    data = {
        "roots": {
            "bookmark_bar": {
                "name": "Bookmarks Bar",
                "type": "folder",
                "children": [
                    {"type": "url", "name": "OpenAI", "url": "https://openai.com"}
                ],
            }
        }
    }
    html = chrome_json_to_html(data)
    assert "OpenAI" in html
    assert "https://openai.com" in html
    assert "Bookmarks Bar" in html
