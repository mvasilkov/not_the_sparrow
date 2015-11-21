from collections import deque
from html import unescape

from hypothesis import given, example
from hypothesis.strategies import text

from not_the_sparrow.util import escape_html, save_html, load_html


@given(string=text())
@example(string='octet = (octet << 1) & 0xff')
def check_escape_html(string):
    assert unescape(escape_html(string)) == string


def check_save_html():
    a, b = save_html('<code>nobody</code> here but us chickens')
    assert a == '<\b> here but us chickens'
    assert b.pop() == '<code>nobody</code>'


def check_load_html():
    b = deque(['chickens'])
    a = load_html('nobody here but us <\b>', b)
    assert a == 'nobody here but us chickens'


@given(string=text())
@example(string='<code>chickens</code>')
def check_save_load(string):
    a, b = save_html(string)
    assert load_html(a, b) == string
