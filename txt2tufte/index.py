import os
import random
import string

from txt2tufte import tufte


def format(data):
    data = tufte.emdash_to_html(data)
    data = tufte.code_to_html(data)
    data = tufte.bold_to_html(data)
    data = tufte.italic_to_html(data)
    data = tufte.un_escape(data)
    return data


def add_articles(data):
    src = os.getenv("INDEX_SRC", "src")
    for article_fn in data.strip().split("\n"):
        if not article_fn:
            continue
        id = "".join(random.choices(string.ascii_lowercase, k=5))
        with open(f"{src}/{article_fn}") as f:
            title = f.readline()
            desc = f.readline()
        desc = format(desc)
        print(
            '<div class="wrap-collapsible">'
            f'<input id="{id}" class="toggle" type="checkbox">'
            f'<label for="{id}" class="lbl-toggle no-underline">'
            f'<a href="{article_fn.split(".")[0]}.html">'
            f'{title}</a></label>'
            '<div class="collapsible-content">'
            '<blockquote class="content-inner">'
            f"{desc}"
            "</blockquote>"
            "</div>"
            "</div>")


def main(data):

    # first three lines (including empty line before menu items)
    title, subtitle, _, data = data.split("\n", 3)

    print(
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<head>"
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<link rel="stylesheet" href="css/tufte.css"/>'
        '<link rel="stylesheet" href="css/tufte-index.css"/>'
        f"<title>{title}</title>"
        "</head>"
        "<body>"
        '<nav class="menu">'
        '<ul class="menu-left">'
        f"<li>{title}</li>"
        "</ul>"
        '<ul class="menu-right">')

    # menu items (if any) followed by empty line
    while True:
        line, data = data.split("\n", 1)
        if not line.strip():
            break
        name, _ = line.split(".", 1)
        print(
            '<li class="no-underline">'
            f'<a class="menu-right-link" href="{name}.html">'
            f'{name.capitalize()} </a></li>')

    print(
        "</ul>"
        "</nav>"
        f'<p class="subtitle">{subtitle}</p>')

    add_articles(data)

    print(
        "</body>"
        "</html>")


if __name__ == "__main__":
    import sys
    main(sys.stdin.read())
