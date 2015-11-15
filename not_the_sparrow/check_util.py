from html import unescape

from hypothesis import given
from hypothesis.strategies import text

from not_the_sparrow import escape_html


@given(string=text())
def check_escape_html(string):
    assert unescape(escape_html(string)) == string
