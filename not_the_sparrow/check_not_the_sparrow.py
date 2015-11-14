from not_the_sparrow import inline_commands

def check_inline_nop():
    assert inline_commands('') == ''
    assert (inline_commands('nobody here but us chickens') ==
            'nobody here but us chickens')

def check_inline_basic():
    assert (inline_commands(r'normal \b{bold} normal') ==
            inline_commands(r'normal \bold{bold} normal') ==
            inline_commands(r'normal \ж{bold} normal') ==
            inline_commands(r'normal \жирный{bold} normal') ==
            'normal <b>bold</b> normal')
    assert (inline_commands(r'normal \i{italic} normal') ==
            inline_commands(r'normal \italic{italic} normal') ==
            inline_commands(r'normal \к{italic} normal') ==
            inline_commands(r'normal \курсив{italic} normal') ==
            'normal <i>italic</i> normal')

def check_inline_begin_end():
    assert inline_commands(r'\b{begin} normal') == '<b>begin</b> normal'
    assert inline_commands(r'normal \к{end}') == 'normal <i>end</i>'
    assert inline_commands(r'\ж{begin}\i{end}') == '<b>begin</b><i>end</i>'
    assert inline_commands(r'\жирный{begin_end}') == '<b>begin_end</b>'
