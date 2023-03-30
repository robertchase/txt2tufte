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
    for article in data.split("\n\n"):
        id = "".join(random.choices(string.ascii_lowercase, k=5))
        fn, desc = article.split("\n", 1)
        with open(f"{src}/{fn}.txt") as f:
            title = f.readline()
        print(
            '<div class="wrap-collapsible">'
            f'<input id="{id}" class="toggle" type="checkbox">'
            f'<label for="{id}" class="lbl-toggle">'
            f'<a class="article-link" href="{fn}.html">{title}</a></label>'
            '<div class="collapsible-content">'
            '<blockquote class="content-inner">'
            f"{desc}"
            "</blockquote>"
            "</div>"
            "</div>")


def main(data):

    title, subtitle, data = data.split("\n", 2)

    print(
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<head>"
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<link rel="stylesheet" href="css/index.css"/>'
        f"<title>{title}</title>"
        "</head>"
        "<body>"
        '<nav class="menu">'
        '<ul class="menu-left">'
        f"<li>{title}</li>"
        "</ul>"
        '<ul class="menu-right">'
        '<li><a class="menu-right-link" href="about.html">About </a></li>'
        '<li><a class="menu-right-link" href="colophon.html">Colophon</a></li>'
        "</ul>"
        "</nav>"
        f'<p class="subtitle">{subtitle}</p>')

    data = format(data.strip())
    data = add_articles(data)

    print(
        "</body>"
        "</html>")


if __name__ == "__main__":
    import sys
    main(sys.stdin.read())
