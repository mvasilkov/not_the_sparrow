from io import StringIO
from re import compile

OPENING = {}
CLOSING = {}

_commands = {
    'b': 'b',
    'bold': 'b',
    'i': 'i',
    'italic': 'i',
    'ж': 'b',
    'жирный': 'b',
    'к': 'i',
    'курсив': 'i',
}

for a, b in _commands.items():
    OPENING[a] = '<%s>' % b
    CLOSING[a] = '</%s>' % b

RE_BEGIN = compile(r'\\(%s)({|{{{)' % '|'.join(_commands.keys()))

del _commands

class Command:
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

class Buffer:
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

class Clip:
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
