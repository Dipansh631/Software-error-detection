import re
from typing import Dict


CONTROL_KEYWORDS = re.compile(r"\b(if|elif|for|while|and|or|case|except|catch|&&|\|\|)\b")


def analyze_code(code_text: str) -> Dict[str, float]:
    """Compute simple static-analysis-like metrics from source code text.

    This is a lightweight heuristic suitable for demo purposes only.
    Metrics:
      - loc: number of non-empty lines
      - num_comments: number of lines starting with '#', '//' or containing '/*'
      - num_functions: count of occurrences of typical function signatures (very heuristic)
      - cyclomatic_complexity_estimate: count of control-flow-ish tokens
      - avg_line_length: average length across non-empty lines
      - num_todos: occurrences of TODO/FIXME tags (used as warnings proxy)
    """
    lines = code_text.splitlines()
    non_empty_lines = [ln for ln in lines if ln.strip()]
    loc = float(len(non_empty_lines))

    # Comments in multiple languages
    comment_line_starts = ("#", "//")
    num_comments = 0
    for ln in lines:
        stripped = ln.strip()
        if any(stripped.startswith(prefix) for prefix in comment_line_starts) or "/*" in stripped:
            num_comments += 1

    # Very rough function detection (works for Python/JS/C-like)
    function_patterns = [
        re.compile(r"\bdef\s+\w+\s*\("),
        re.compile(r"\bfunction\s+\w+\s*\("),
        re.compile(r"\b\w+\s+\w+\s*\(.*\)\s*\{"),  # C-like returns
    ]
    num_functions = 0
    for pat in function_patterns:
        num_functions += len(pat.findall(code_text))

    # Complexity proxy: count of control tokens
    complexity_tokens = CONTROL_KEYWORDS.findall(code_text)
    cyclomatic_complexity_estimate = float(len(complexity_tokens)) + 1.0  # +1 as a baseline

    # Average line length across non-empty lines
    if non_empty_lines:
        avg_line_length = sum(len(ln) for ln in non_empty_lines) / float(len(non_empty_lines))
    else:
        avg_line_length = 0.0

    # TODO/FIXME warnings proxy
    num_todos = float(len(re.findall(r"\b(TODO|FIXME)\b", code_text, flags=re.IGNORECASE)))

    return {
        "loc": loc,
        "num_comments": float(num_comments),
        "num_functions": float(num_functions),
        "cyclomatic_complexity_estimate": float(cyclomatic_complexity_estimate),
        "avg_line_length": float(avg_line_length),
        "num_todos": float(num_todos),
    }


