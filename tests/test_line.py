import pytest

import tufte


@pytest.mark.parametrize("data, result", (
    ("section data", "section data"),
    ("section--data", "section&mdash;data"),
    ("section --data", "section&mdash;data"),
    ("section-- data", "section&mdash;data"),
    ("section -- data", "section&mdash;data"),
    ("section  --  data", "section &mdash; data"),
    ("\nsection--data\nmore--data", "\nsection&mdash;data\nmore&mdash;data"),
    ("section\n--data", "section&mdash;data"),
    ("section\n--\ndata", "section&mdash;data"),
))
def test_emdash(data, result):
    assert tufte.emdash_to_html(data) == result


@pytest.mark.parametrize("data, result", (
    ("section data", "section data"),
    ("section `code` data", "section <code>code</code> data"),
    ("section`code`data", "section<code>code</code>data"),
    ("\na `b` c\nd `e` f\n",
     "\na <code>b</code> c\nd <code>e</code> f\n"),
))
def test_code(data, result):
    assert tufte.code_to_html(data) == result


@pytest.mark.parametrize("data, result", (
    ("section data", "section data"),
    ("section **exciting** data", "section <b>exciting</b> data"),
    ("\na **b** c\nd **e** f\n", "\na <b>b</b> c\nd <b>e</b> f\n"),
    ("section *not** data", "section *not** data"),
    ("section ***extra*** data", "section <b>*extra</b>* data"),
))
def test_bold(data, result):
    assert tufte.bold_to_html(data) == result


@pytest.mark.parametrize("data, result", (
    ("section data", "section data"),
    ("section *interesting* data", "section <em>interesting</em> data"),
    ("\na *b* c\nd *e* f\n", "\na <em>b</em> c\nd <em>e</em> f\n"),
    ("section *not data", "section *not data"),
    ("section *sorta** data", "section <em>sorta</em>* data"),
))
def test_italic(data, result):
    assert tufte.italic_to_html(data) == result


@pytest.mark.parametrize("data, result", (
    ("section data", "section data"),
    ("section\n## heading\ndata", "section<h3>heading</h3>\n\ndata"),
    ("section\n### heading\ndata", "section<h4>heading</h4>\n\ndata"),
))
def test_heading(data, result):
    assert tufte.heading_to_html(data) == result
