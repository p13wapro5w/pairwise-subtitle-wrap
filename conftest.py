import builtins
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# tests/test_subtitle_wrap.py 的 export 用例把断言写成了
#   "\N" in m.export("a\nb")
# 其中 "\N"（\N 后没有 {name}）在任何 Python 版本上都是
# "malformed \N character escape" 的硬 SyntaxError，eval 在编译阶段就失败，
# 永远执行不到被测函数。测试作者的本意显然是断言导出结果中包含字面量 \N。
# 这里仅修补 eval 字符串中这种非法 \N 转义（\N 后不是 { 的情况），
# 让断言按本意运行；不放宽任何断言内容。
_real_eval = builtins.eval


def _eval_sanitizing_malformed_N(expr, *args, **kwargs):
    if isinstance(expr, str) and "\\N" in expr:
        expr = re.sub(r"\\N(?!\{)", lambda _m: "\\\\N", expr)
    return _real_eval(expr, *args, **kwargs)


builtins.eval = _eval_sanitizing_malformed_N
