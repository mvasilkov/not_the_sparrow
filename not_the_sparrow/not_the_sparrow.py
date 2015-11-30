from io import StringIO
from re import compile as re_compile

from .util import escape_html

OPENING = {}
CLOSING = {}

_commands = {
    'b': 'b',
    'i': 'i',
    'ж': 'b',
    'к': 'i',
}

for a, b in _commands.items():
    OPENING[a] = '<%s>' % b
    CLOSING[a] = '</%s>' % b

RE_BEGIN = re_compile(r'\\(%s)({{{|{)' % '|'.join(_commands.keys()))

del _commands

RE_INDENT = re_compile(' {4}| {0,3}\t')


class Command(object):
    _closed = False

    def __init__(self, command, length):
        self._command = command
        self.length = length

    def opening_tag(self):
        return OPENING[self._command]

    def closing_tag(self):
        return CLOSING[self._command]

    def close(self):
        self._closed = True
        return self.closing_tag()

    def __str__(self):
        return self.opening_tag() if self._closed else ''


def _stringify(a):
    if isinstance(a, StringIO):
        b = a.getvalue()
        a.close()
        return b
    return str(a)


class Buffer(object):
    _peek = None

    def __init__(self):
        self._clip = []

    def push(self, a):
        if isinstance(a, str):
            if isinstance(self._peek, StringIO):
                self._peek.write(a)
            else:
                b = StringIO()
                b.write(a)
                self._clip.append(b)
                self._peek = b
        else:
            self._clip.append(a)
            self._peek = a

    def __str__(self):
        return ''.join(_stringify(a) for a in self._clip)


class Clip(object):
    peek = None

    def __init__(self):
        self._clip = []

    def push(self, a):
        self._clip.append(a)
        self.peek = a

    def pop(self):
        a = self._clip.pop()
        self.peek = self._clip[-1] if self._clip else None
        return a


def inline_commands(a):
    buf = Buffer()
    clip = Clip()
    i = 0
    while i < len(a):
        begin = RE_BEGIN.match(a[i:])
        if begin:
            cmd = Command(begin.group(1), len(begin.group(2)))
            clip.push(cmd)
            buf.push(cmd)
            i += begin.span()[1]
            continue

        b = a[i]
        if b == '}' and clip.peek:
            if clip.peek.length == 3 and a[i:].startswith('}}}'):
                i += 2

            buf.push(clip.pop().close())
        else:
            buf.push(b)

        i += 1

    return str(buf)


class Line(object):
    _string = None
    _monospaced = False

    def __init__(self, string):
        if string and not string.isspace():
            indent = RE_INDENT.match(string)
            if indent is None:
                self._string = string.strip()
            else:
                self._string = string[indent.span()[1]:]
                self._monospaced = True

    def __bool__(self):
        return self._string is not None

    def __str__(self):
        if self._monospaced:
            return '<code>%s</code>' % self._string
        return '' if self._string is None else self._string


class Prose(Clip):
    def push(self, a):
        if not self.peek and not a:
            return
        super().push(a)

    def __bool__(self):
        return bool(self._clip)

    def __str__(self):
        return '<br>\n'.join(str(a) for a in self._clip)


def break_lines(a):
    prose = Prose()
    for string in escape_html(a).splitlines():
        prose.push(Line(string))

    if prose and not prose.peek:
        prose.pop()

    return str(prose)
