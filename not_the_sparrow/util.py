from collections import deque
import re

RE_SAVE_BLOCK = re.compile('<code>.*?</code>')
RE_LOAD_BLOCK = re.compile('<\b>')


def escape_html(string):
    '''
    Returns the given string with ampersands and angle brackets
    encoded for use in HTML.
    '''
    return (string
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;'))


def save_blocks(string):
    blocks = deque()

    def _save_block(x):
        blocks.append(x.group(0))
        return '<\b>'

    string = RE_SAVE_BLOCK.sub(_save_block, string)
    return string, blocks


def load_blocks(string, blocks):
    def _load_block(x):
        return blocks.popleft()
    return RE_LOAD_BLOCK.sub(_load_block, string)
