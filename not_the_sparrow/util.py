from collections import deque
from re import compile

RE_SAVE = compile('<code>.*?</code>')
RE_LOAD = compile('<\b>')


def escape_html(string):
    '''
    Returns the given string with ampersands and angle brackets
    encoded for use in HTML.
    '''
    return (string
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;'))


def save_html(string):
    blocks = deque()

    def _save_block(x):
        blocks.append(x.group(0))
        return '<\b>'

    string = RE_SAVE.sub(_save_block, string)
    return string, blocks


def load_html(string, blocks):
    def _load_block(x):
        return blocks.popleft()
    return RE_LOAD.sub(_load_block, string)
