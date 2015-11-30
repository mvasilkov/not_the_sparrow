from ctypes import CDLL, c_char_p, c_long
from re import compile as re_compile

from hypothesis import given, example
from hypothesis.strategies import text

from not_the_sparrow import break_lines

cmark = CDLL('libcmark.dylib')

cmark_markdown_to_html = cmark.cmark_markdown_to_html
cmark_markdown_to_html.argtypes = (c_char_p, c_long, c_long)
cmark_markdown_to_html.restype = c_char_p

RE_COMMONMARK_P = re_compile('<p>(.*?)</p>')
RE_COMMONMARK_CODE = re_compile('<pre><code>(.*)')

spaces = (' ', '\t')


def commonmark(string):
    bytestring = string.encode('utf8')
    length = len(bytestring)
    return cmark_markdown_to_html(bytestring, length, 0).decode('utf8')


def assert_likeness(string):
    a = break_lines(string)
    b = commonmark(string)

    if not b:
        assert not a
        assert not string or string.isspace()
        return

    if b.startswith('<p>'):
        assert not a.startswith('<code>')
        wrapped = RE_COMMONMARK_P.match(b)
        assert wrapped
        assert a == wrapped.group(1)
    else:
        assert a.startswith('<code>')
        wrapped = RE_COMMONMARK_CODE.match(b)
        assert wrapped
        assert a == '<code>%s</code>' % wrapped.group(1)


@given(before=text(alphabet=spaces), after=text(alphabet=spaces))
@example(before='\t\t', after='')
def test_indent_commonmark(before, after):
    string = 'chickens'.join([before, after])
    assert_likeness(string)


@given(string=text(alphabet=('x', *spaces)))
@example(string='x'.join(4 * (4 * ' ',)))
def test_spaces_commonmark(string):
    assert_likeness(string)
