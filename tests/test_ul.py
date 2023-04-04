import pytest

from txt2tufte import tufte


@pytest.mark.parametrize("data, result", (
    ("abc\ndef", "abc\ndef"),
    ("abc\n@def\nghi", "abc<ul><li>def</li></ul>ghi"),
    ("abc\n@def\n@ghi\njkl", "abc<ul><li>def</li><li>ghi</li></ul>jkl"),
    ("abc\n@def\n@ghi\njkl\n@mno\npqr",
     "abc<ul><li>def</li><li>ghi</li></ul>jkl<ul><li>mno</li></ul>pqr"),
))
def test_ul(data, result):
    assert tufte.unordered_list_to_html(data) == result
