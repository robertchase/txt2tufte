import random
import re
import string


def emdash_to_html(data):
    pat = r"(.*?)\s?--\s?(.*)"
    while m := re.match(pat, data, re.DOTALL):
        data = f"{m.group(1)}&mdash;{m.group(2)}"
    return data


def code_to_html(data):
    pat = r"(.*?)`(.*?)`(.*)"
    while m := re.match(pat, data, re.DOTALL):
        data = f"{m.group(1)}<code>{m.group(2)}</code>{m.group(3)}"
    return data


def bold_to_html(data):
    pat = r"(.*?)(?<!\\)\*{2}(.+?)(?<!\\)\*{2}(.*)"  # 2 non-escaped *s
    while m := re.match(pat, data, re.DOTALL):
        data = f"{m.group(1)}<b>{m.group(2)}</b>{m.group(3)}"
    return data


def italic_to_html(data):
    pat = r"(.*?)(?<!\\)\*(.+?)(?<!\\)\*(.*)"  # non escaped *
    while m := re.match(pat, data, re.DOTALL):
        data = f"{m.group(1)}<em>{m.group(2)}</em>{m.group(3)}"
    return data


def link_to_html(data):
    pat = r"(.*?)\[(.+?)\]\((.+?)\)(.*)"
    while m := re.match(pat, data, re.DOTALL):
        data = (
            f"{m.group(1)}"
            f'<a href="{m.group(3)}">{m.group(2)}</a>'
            f"{m.group(4)}")
    return data


def uppercase_to_html(data):
    pat = r"(.*?)\n\+(.+?)\n(.*)"
    while m := re.match(pat, data, re.DOTALL):
        data = (
            f"{m.group(1)}"
            f'\n\n<span class="newthought">{m.group(2)}</span>\n'
            f"{m.group(3)}")
    return data


def heading_to_html(data):
    pat = r"(.*?)\n(#{2,3}) +(.+?)\n(.*)"
    while m := re.match(pat, data, re.DOTALL):
        level = len(m.group(2)) + 1
        data = (
            f"{m.group(1)}"
            f"<h{level}>{m.group(3)}</h{level}>"
            f"\n\n{m.group(4)}")
    return data


def split(data, divider):
    parts = data.split(divider, 2)
    if len(parts) == 3:
        before, middle, after = parts
        if len(middle):
            return before, middle, after
    return None, None, None


def margin(span_cls, text, note,
           label_cls="", before_span=""):
    id = "".join(random.choices(string.ascii_lowercase, k=5))
    return (
        f' <label for="{id}" class="margin-toggle {label_cls}">'
        f'{text}</label>'
        f'<input type="checkbox" id="{id}" class="margin-toggle"/>'
        f"{before_span}"
        f'<span class="{span_cls}">{note}</span>')


def footnote_to_html(section):
    while True:
        before, note, after = split(section, "\n^")
        if before:
            if note[0] == "\n":
                text = ""
            else:
                text, note = note.split("\n", 1)
            section = before + margin(
                "sidenote", text, note, "sidenote-number") + after
        else:
            break
    return section


def marginnote_to_html(section):
    while True:
        before, note, after = split(section, "\n>")
        if before:
            section = before + margin(
                "marginnote", "&#8853;", note) + after
        else:
            break
    return section


def image_to_html(section):
    while True:
        before, note, after = split(section, "\n{")
        if before:
            url, note = note.split("\n", 1)
            img = f'<img src="{url}">'
            section = before + "<figure>" + margin(
                "marginnote", "&#8853;", note,
                before_span=img) + "</figure>" + after
        else:
            break
    return section


def marginimage_to_html(section):
    while True:
        before, note, after = split(section, "\n}")
        if before:
            url, note = note.split("\n", 1)
            img = f'<img src="{url}">'
            section = before + margin(
                "marginnote", "&#8853;", img + note) + after
        else:
            break
    return section


def section_title(section):
    if section[0] != "\n":
        if "\n" in section:
            title, new_section = section.split("\n", 1)
            if title:
                return f"<h2>{title}</h2><p>{new_section}</p>"
    return f"<p>{section}</p>"


def section_to_html(section):
    section = section_title(section)
    section = emdash_to_html(section)
    section = code_to_html(section)
    section = bold_to_html(section)
    section = italic_to_html(section)
    section = link_to_html(section)
    section = uppercase_to_html(section)
    section = footnote_to_html(section)
    section = marginnote_to_html(section)
    section = image_to_html(section)
    section = marginimage_to_html(section)
    section = re.sub(r"\n{2,}", "</p><p>", section)
    return f"<section>{section}</section>"


def main(data):

    title, author, date, data = data.split("\n", 3)

    print(
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<head>"
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<link rel="stylesheet" href="tufte.css"/>'
        f"<title>{title}</title>"
        "</head>"
        "<body>"
        "<article>"
        f"<h1>{title}</h1>"
        f'<p class="subtitle">{author}<br>{date}</p>')

    data = heading_to_html(data)
    for section in re.split(r"\n#", data):
        if section.strip():
            print(section_to_html(section))

    print(
        "</article>"
        "</body>"
        "</html>")


if __name__ == "__main__":
    import sys
    main(sys.stdin.read())
