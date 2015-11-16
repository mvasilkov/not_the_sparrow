from html import unescape

from hypothesis import given, example
from hypothesis.strategies import text

from not_the_sparrow import escape_html


@given(string=text())
@example(string='octet = (octet << 1) & 0xff')
def check_escape_html(string):
    assert unescape(escape_html(string)) == string
