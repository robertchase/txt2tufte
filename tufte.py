import random
import re
import string


def to_lines(data):
    """break data into list of lines"""
    result = []
    for line in data.split("\n"):
        if line := line.strip():
            result.append(line)
        elif result:  # ignore empty lines at top of file
            if result[-1]:  # ignore duplicate empty lines
                result.append("")
    return result


def to_paragraphs(lines):
    """break list of lines into list of paragraphs (list of list of lines)"""
    result = []
    paragraph = []
    for line in lines:
        if line:
            paragraph.append(line)
        else:
            if paragraph:  # do we have anything to add?
                result.append(paragraph)
                paragraph = []
    if paragraph:
        result.append(paragraph)

    return result


def to_sections(paragraphs):
    """break paragraphs into sections (sections start with "#")

    a section is a list of paragraphs
    a paragraph is a list of lines
    """

    def is_section(line):
        if line == "#":
            return True
        if line.startswith("# "):
            return True
        return False

    first_para = paragraphs[0]
    if not is_section(first_para[0]):
        first_para.insert("#", 0)  # force section header as first line

    result = []
    section = []

    for paragraph in paragraphs:
        if is_section(paragraph[0]):
            if section:
                result.append(section)
                section = []
            section.append(paragraph)
        else:
            section.append(paragraph)

    if section:
        result.append(section)
    return result


def lines_to_html(lines):
    """multi-line conversions"""
    is_note = False
    result = []
    for line in lines:

        # ^ optional text to which footnote is attached
        # numbered side note
        # numbered side note
        # ^
        if line.startswith("^"):
            if is_note:
                result.append("</span>")
                is_note = False
            else:
                is_note = True
                toks = line.split(maxsplit=1)
                text = toks[1] if len(toks) > 1 else ""
                id = "sn-" + ''.join(
                    random.choices(string.ascii_lowercase, k=5))
                result.append(
                    f'<label for="{id}" class="margin-toggle sidenote-number">'
                    f'{text}</label>'
                    f'<input type="checkbox" id="{id}" class="margin-toggle"/>'
                    '<span class="sidenote">'
                )

        # >
        # side note
        # side note
        # >
        elif line == ">":
            if is_note:
                result.append("</span>")
                is_note = False
            else:
                is_note = True
                id = "mn-" + ''.join(
                    random.choices(string.ascii_lowercase, k=5))
                result.append(
                    f'<label for="{id}" class="margin-toggle">'
                    f'&#8853;</label>'
                    f'<input type="checkbox" id="{id}" class="margin-toggle"/>'
                    '<span class="marginnote">'
                )

        # image with margin text
        #
        # { image url
        # margin text
        # {
        elif m := re.match(r"{\s(.+)$", line):
            if is_note:
                result.append("</span>")
                is_note = False
            else:
                is_note = True
                id = "im-" + ''.join(
                    random.choices(string.ascii_lowercase, k=5))
                result.append(
                    "<figure>"
                    f'<label for="{id}" class="margin-toggle">'
                    f'&#8853;</label>'
                    f'<input type="checkbox" id="{id}" class="margin-toggle"/>'
                    f'<img src="{m.group(1)}">'
                    '<span class="marginnote">'
                )
        elif line == "{":
            if not is_note:
                raise Exception("unexpected image end")
            is_note = False
            result.append("</span></figure>")

        # margin image
        #
        # } image url
        # additional text
        # }
        elif m := re.match(r"}\s(.+)$", line):
            if is_note:
                result.append("</span>")
                is_note = False
            else:
                is_note = True
                id = "mi-" + ''.join(
                    random.choices(string.ascii_lowercase, k=5))
                result.append(
                    f'<label for="{id}" class="margin-toggle">'
                    f'&#8853;</label>'
                    f'<input type="checkbox" id="{id}" class="margin-toggle"/>'
                    '<span class="marginnote">'
                    f'<img src="{m.group(1)}">'
                )
        elif line == "}":
            if not is_note:
                raise Exception("unexpected margin image end")
            is_note = False
            result.append("</span>")

        else:
            result.append(line)

    if is_note:
        raise Exception("unmatched marginnote or sidenote")
    return result


def line_to_html(line):
    """perform one-line transformations"""

    # em dash --
    while m := re.match(r"(.*?)\s?--\s?(.*)$", line):
        line = m.group(1) + "&mdash;" + m.group(2)

    # code `
    while m := re.match(r"(.*?)`(.+?)`(.*)$", line):
        line = f"{m.group(1)}<code>{m.group(2)}</code>{m.group(3)}"

    # bold **
    while m := re.match(r"(.*?)\*\*(.+?)\*\*(.*)$", line):
        line = f"{m.group(1)}<b>{m.group(2)}</b>{m.group(3)}"

    # italics *
    while m := re.match(r"(.*?)\*(.+?)\*(.*)$", line):
        line = f"{m.group(1)}<em>{m.group(2)}</em>{m.group(3)}"

    # link [name](url)
    while m := re.match(r"(.*?)\[(.*?)\]\((.*?)\)(.*)$", line):
        line = (
            f"{m.group(1)}"
            f'<a href="{m.group(3)}">{m.group(2)}</a>'
            f"{m.group(4)}")

    return line


def to_html(sections):
    """change sections to list of html"""
    result = []
    for section in sections:
        result.append("<section>")

        first_para = section[0]
        first_line = first_para[0]

        # add section heading if provided after "#"
        toks = first_line.split(maxsplit=1)
        if len(toks) > 1:
            result.append(f"<h2>{toks[1]}</h2>")

        # remove first line in section (the "# ...")
        first_para = first_para[1:]
        if not first_para:  # is first paragraph empty now?
            section = section[1:]
            first_para = section[0]

        # start section with UPPERCASE WORDS (supplied after "+")
        if first_para[0].startswith("+"):
            first_para[0] = (
                '<span class="newthought">'
                f"{section[0][0][1:]}</span>")

        for paragraph in section:
            result.append("<p>")
            for line in paragraph:
                result.append(line_to_html(line))
            result.append("</p>")

        result.append("</section>")
        result = lines_to_html(result)
    return "\n".join(result)


def main(data):

    # do some normalization to make to_html less flagy
    lines = to_lines(data)
    title, author, date, lines = lines[0], lines[1], lines[2], lines[3:]
    paragraphs = to_paragraphs(lines)
    sections = to_sections(paragraphs)

    content = to_html(sections)
    with open("article.html") as article:
        data = article.read()
    print(data.format(title=title, author=author, date=date, content=content))


if __name__ == "__main__":
    import sys
    main(sys.stdin.read())
