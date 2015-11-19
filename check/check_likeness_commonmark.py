from ctypes import CDLL, c_char_p, c_long
from re import compile, MULTILINE

from hypothesis import given
from hypothesis.strategies import text

from not_the_sparrow import break_lines

cmark = CDLL('libcmark.dylib')

cmark_markdown_to_html = cmark.cmark_markdown_to_html
cmark_markdown_to_html.argtypes = (c_char_p, c_long, c_long)
cmark_markdown_to_html.restype = c_char_p

RE_COMMONMARK_CODE = compile('<pre><code>(.*)', MULTILINE)


def commonmark(string):
    bytestring = string.encode('utf8')
    length = len(bytestring)
    return cmark_markdown_to_html(bytestring, length, 0).decode('utf8')


@given(string=text(alphabet=(' ', '\t')))
def check_break_indent_commonmark(string):
    string += 'chickens'
    a = break_lines(string)
    b = commonmark(string)

    if b.startswith('<p>'):
        assert not a.startswith('<code>')
    else:
        wrapped = RE_COMMONMARK_CODE.match(b)
        assert wrapped
        assert a == '<code>%s</code>' % wrapped.group(1)
