from glob import glob
import re
import sys

from not_the_sparrow import to_html


def make_fn(name, before, after):
    def fn():
        assert after[-1] == '\n'
        assert to_html(before) == after[:-1]

    setattr(sys.modules[__name__], 'test_' + name, fn)

for name in glob('sample/*.txt'):
    with open(name, encoding='utf8') as f:
        parts = re.split('^----*\n', f.read(), flags=re.MULTILINE)
        assert len(parts) == 2
        make_fn(name[7:-4], *parts)
