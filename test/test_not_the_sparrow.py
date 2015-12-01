from string import whitespace

from hypothesis import given
from hypothesis.strategies import text

from not_the_sparrow import to_html
from not_the_sparrow.not_the_sparrow import inline_commands, break_lines


def test_inline_nop():
    assert inline_commands('') == ''
    assert (inline_commands('nobody here but us chickens') ==
            'nobody here but us chickens')


def test_break_nop():
    assert break_lines('') == ''
    assert (break_lines('nobody here but us chickens') ==
            'nobody here but us chickens')


@given(string=text())
def test_nonchalant_hypothesis(string):
    assert isinstance(inline_commands(string), str)
    assert isinstance(break_lines(string), str)
    assert isinstance(to_html(string), str)


def test_inline_basic():
    for b in (('{', '}'), ('{{{', '}}}')):
        for a in ('b', 'ж'):
            assert (inline_commands(
                'nobody \\%s%s chickens %s nobody' % (a, *b)) ==
                'nobody <b> chickens </b> nobody')

        for a in ('i', 'к'):
            assert (inline_commands(
                'nobody \\%s%s chickens %s nobody' % (a, *b)) ==
                'nobody <i> chickens </i> nobody')


def test_inline_begin_end():
    for b in (('{', '}'), ('{{{', '}}}')):
        assert (inline_commands(
            '\\b%s chickens %s nobody' % b) ==
            '<b> chickens </b> nobody')
        assert (inline_commands(
            'nobody \\b%s chickens %s' % b) ==
            'nobody <b> chickens </b>')
        assert (inline_commands(
            '\\b%s nobody %s \\b%s chickens %s' % (*b, *b)) ==
            '<b> nobody </b> <b> chickens </b>')
        assert (inline_commands(
            '\\b%s chickens %s' % b) ==
            '<b> chickens </b>')


def test_inline_nested():
    assert (inline_commands(
        '\\b{{{\\i{\\i{\\i{ chickens }}}}}}') ==
        '<b><i><i><i> chickens </i></i></i></b>')
    assert (inline_commands(
        '\\i{\\b{{{\\i{\\i{ chickens }}}}}}') ==
        '<i><b><i><i> chickens </i></i></b></i>')
    assert (inline_commands(
        '\\i{\\i{\\b{{{\\i{ chickens }}}}}}') ==
        '<i><i><b><i> chickens </i></b></i></i>')
    assert (inline_commands(
        '\\i{\\i{\\i{\\b{{{ chickens }}}}}}') ==
        '<i><i><i><b> chickens </b></i></i></i>')


def njoin(*args):
    return '\n'.join(args)


@given(string=text(alphabet=whitespace))
def test_break_ignore(string):
    assert break_lines(string) == ''
    assert (break_lines(njoin(string, 'chickens')) ==
            break_lines(njoin('chickens', string)) ==
            break_lines(njoin(string, 'chickens', string)) ==
            'chickens')


def test_break_indent():
    for x in range(4):
        a = x * ' ' + 'chickens'
        assert break_lines(a) == a.lstrip()

    for x in range(4, 10):
        a = x * ' ' + 'chickens'
        assert break_lines(a) == '<code>%s</code>' % a[4:]


def test_to_html_nop():
    assert to_html('') == ''
    assert (to_html('nobody here but us chickens') ==
            'nobody here but us chickens')
