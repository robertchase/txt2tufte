import random
import re
import string


def return_arrow_to_html(data):
    return re.sub(
        "\n<=\n?",
        '<p class="no-underline"><a href="index.html">&larr;</a></p>\n',
        data)


def horizontal_rule_to_html(data):
    return re.sub(r"\n---\n", "\n<hr>\n", data)


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
    pat = r"(.*?)(?<!\\)\[(.+?)(?<!\\)\](?<!\\)\((.+?)(?<!\\)\)(.*)"
    while m := re.match(pat, data, re.DOTALL):
        data = (
            f"{m.group(1)}"
            f'<a href="{m.group(3)}">{m.group(2)}</a>'
            f"{m.group(4)}")
    return data


def unordered_list_to_html(data):

    def find_unorderd_list(data):
        res = data.split("\n@", 1)
        if len(res) == 2:
            beg, data = res
            res = re.split("\n(?!@)", data, 1)
            if len(res) == 2:
                return beg, res[0], res[1]
        return None

    while m := find_unorderd_list(data):
        items = m[1].rstrip().split("\n@")
        items = "".join(f"<li>{item}</li>" for item in items)
        data = f"{m[0]}<ul>{items}</ul><p>{m[2]}"
    return data


def un_escape(data):
    data = re.sub(r"\\\*", "*", data, re.DOTALL)

    data = re.sub(r"\\\(", "(", data, re.DOTALL)
    data = re.sub(r"\\\)", ")", data, re.DOTALL)

    data = re.sub(r"\\\[", "[", data, re.DOTALL)
    data = re.sub(r"\\\]", "]", data, re.DOTALL)

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


def blockquote_to_html(section):
    while True:
        before, quote, after = split(section, "\n%")
        if before:
            ref, quote = quote.split("\n", 1)
            section = (
                f"{before}<blockquote><p>{quote}</p>"
                f"<footer>{ref}</footer></blockquote>{after}"
            )
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
    section = horizontal_rule_to_html(section)
    section = emdash_to_html(section)
    section = code_to_html(section)
    section = bold_to_html(section)
    section = italic_to_html(section)
    section = link_to_html(section)
    section = un_escape(section)
    section = unordered_list_to_html(section)
    section = uppercase_to_html(section)
    section = footnote_to_html(section)
    section = marginnote_to_html(section)
    section = blockquote_to_html(section)
    section = image_to_html(section)
    section = marginimage_to_html(section)
    section = re.sub(r"\n{2,}", "</p><p>", section)
    return f"<section>{section}</section>"


def main(data):

    title, _, author, date, data = data.split("\n", 4)

    print(
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<head>"
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<link rel="stylesheet" href="css/tufte.css"/>'
        '<link rel="stylesheet" href="css/tufte-nav.css"/>'
        f"<title>{title}</title>"
        "</head>"
        "<body>"
        "<article>"
        f"<h1>{title}</h1>"
        '<p class="subtitle no-underline">'
        f'<a href="index.html">&lsaquo; {author}</a><br>{date}</p>')

    data = heading_to_html(data)
    data = return_arrow_to_html(data)
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
