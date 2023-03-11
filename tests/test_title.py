import pytest

import tufte


@pytest.mark.parametrize("data, result", (
    ("section data", "<p>section data</p>"),
    ("\nsection data", "<p>\nsection data</p>"),
    ("\n\n\nsection data\n\n\n", "<p>\n\n\nsection data\n\n\n</p>"),
    ("title\ndata", "<h2>title</h2><p>data</p>"),
))
def test_section_title(data, result):
    assert tufte.section_title(data) == result
