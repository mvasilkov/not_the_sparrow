from collections import deque
from html import unescape

from hypothesis import given, example
from hypothesis.strategies import text

from not_the_sparrow.util import escape_html, save_blocks, load_blocks


@given(string=text())
@example(string='octet = (octet << 1) & 0xff')
def test_escape_html(string):
    assert unescape(escape_html(string)) == string


def test_save_blocks():
    a, b = save_blocks('<code>nobody</code> := <code>chickens</code>')
    assert a == '<\b> := <\b>'
    assert b.pop() == '<code>chickens</code>'
    assert b.pop() == '<code>nobody</code>'


def test_load_blocks():
    b = deque(['nobody', 'chickens'])
    a = load_blocks('<\b> here but us <\b>', b)
    assert a == 'nobody here but us chickens'


@given(string=text())
@example(string='<code>chickens</code>')
def test_save_load_blocks(string):
    a, b = save_blocks(string)
    assert load_blocks(a, b) == string
