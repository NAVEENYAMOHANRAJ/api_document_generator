"""Base parser utilities for extractors."""

from typing import List, Tuple


def tokenize_code(code: str) -> List[str]:
    """Tokenize code while preserving PHP array syntax needed by parsers."""
    import re
    token_pattern = r"""
        '(?:\\.|[^'\\])*'
        |"(?:\\.|[^"\\])*"
        |=>|::|->
        |-?\d+\.\d+|-?\d+
        |[A-Za-z_\\][A-Za-z0-9_\\]*
        |[\[\]\(\),]
    """
    return re.findall(token_pattern, code, flags=re.VERBOSE)


def find_matching_index(tokens: List[str], start: int, open_char: str, close_char: str) -> int:
    """Find matching closing bracket."""
    count = 1
    for i in range(start + 1, len(tokens)):
        if tokens[i] == open_char:
            count += 1
        elif tokens[i] == close_char:
            count -= 1
            if count == 0:
                return i
    return -1


def get_tokens_slice(tokens: List[str], start: int, end: int) -> str:
    """Get slice of tokens as string."""
    return ' '.join(tokens[start:end])
