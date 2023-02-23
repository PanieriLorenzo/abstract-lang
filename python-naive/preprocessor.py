import re

_comment_re = re.compile(r'#.*$', flags=re.MULTILINE)

def preprocess(s: str) -> str:
    """transformations at the string level, with no parsing"""

    s = _comment_re.sub('', s)
    
    s = ' '.join(s
        .replace('\n', ' ')
        .replace('\t', ' ')
        .replace('\r', ' ')
        .split())
    
    return s