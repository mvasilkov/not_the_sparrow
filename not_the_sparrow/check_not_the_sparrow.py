from string import whitespace

from hypothesis import given
from hypothesis.strategies import text

from not_the_sparrow import inline_commands, break_lines


def check_inline_nop():
    assert inline_commands('') == ''
    assert (inline_commands('nobody here but us chickens') ==
            'nobody here but us chickens')


def check_break_nop():
    assert break_lines('') == ''
    assert (break_lines('nobody here but us chickens') ==
            'nobody here but us chickens')


@given(string=text())
def check_nonchalant_hypothesis(string):
    assert isinstance(inline_commands(string), str)
    assert isinstance(break_lines(string), str)


def check_inline_basic():
    for b in (('{', '}'), ('{{{', '}}}')):
        for a in ('b', 'ж'):
            assert (inline_commands(
                'nobody \\%s%s chickens %s nobody' % (a, *b)) ==
                'nobody <b> chickens </b> nobody')

        for a in ('i', 'к'):
            assert (inline_commands(
                'nobody \\%s%s chickens %s nobody' % (a, *b)) ==
                'nobody <i> chickens </i> nobody')


def check_inline_begin_end():
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


@given(string=text(alphabet=whitespace))
def check_break_ignore(string):
    assert break_lines(string) == ''
    assert (break_lines('%s \n' 'chickens' % string) ==
            break_lines('chickens' '\n %s' % string) ==
            'chickens')


def check_break_indent():
    for x in range(4):
        a = x * ' ' + 'chickens'
        assert break_lines(a) == a

    for x in range(4, 10):
        a = x * ' ' + 'chickens'
        assert break_lines(a) == '<code>%s</code>' % a[4:]
