from not_the_sparrow import inline_commands


def check_inline_nop():
    assert inline_commands('') == ''
    assert (inline_commands('nobody here but us chickens') ==
            'nobody here but us chickens')


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
