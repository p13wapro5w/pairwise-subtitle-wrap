import pytest
import math
from media import subtitle_wrap as mod

CASES = [
    ("measure", 'm.measure("abc", 10) == 30'),
    ("wrap", 'm.wrap(6, 20, 10) == 3'),
    ("punct", 'm.punctuation("abc", 1) is True'),
    ("safe", 'm.safe(1920, 1080) == 108'),
    ("duration", 'm.duration("abcd", 2) == 2'),
    ("overlap", 'm.overlap(0, 2, 1) is True'),
    ("anchor", 'm.anchor("center") == "center"'),
    ("scale", 'm.scale(24, 2160) == 48'),
    ("export", '"\\N" in m.export("a\\nb")'),
    ("lang", 'm.language("中文") == "zh"'),
    ("count", 'm.count([1, 2]) == 2'),
    ("clamp", 'm.clamp01(1.2) == 1.0'),
    ("key", 'm.key(1) == "c:1"'),
    ("max", 'm.max_chars(100, 10) == 10'),
    ("wide", 'm.wide("中") is True')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx, "math": math})
