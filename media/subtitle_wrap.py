import math
import unicodedata

# 行首禁则标点（不允许出现在行首的标点）
LEADING_FORBIDDEN = set("。，、；：？！…—）】》」』”’‰·")
# 行尾禁则标点（不允许留在行尾的开括号类）
TRAILING_FORBIDDEN = set("（【《「『“‘")

_ANCHORS = {
    "left", "center", "right",
    "top-left", "top-center", "top-right",
    "bottom-left", "bottom-center", "bottom-right",
}


def wide(char):
    """全角判定。"""
    if not char:
        return False
    return unicodedata.east_asian_width(char[0]) in ("W", "F")


def measure(text, char_width):
    """实际字体测量：按字符逐个量宽，全角字符按两倍宽度计。"""
    total = 0
    for ch in text:
        total += char_width * 2 if wide(ch) else char_width
    return total


def max_chars(width, char_width):
    """单行上限：安全区像素宽度内能放下的字符数。"""
    if char_width <= 0:
        return 0
    return int(width // char_width)


def wrap(length, max_width, char_width):
    """按像素断行：总像素长度 / 行宽，向上取整得行数。"""
    if max_width <= 0 or char_width <= 0 or length <= 0:
        return 0
    return math.ceil(length * char_width / max_width)


def punctuation(text, index):
    """标点禁则：index 处是否允许断行（行首不能是禁则标点）。"""
    if not text or index < 0 or index >= len(text):
        return True
    return text[index] not in LEADING_FORBIDDEN


def safe(width, height):
    """按画幅安全区：底部安全边距，随画幅高度按比例计算。"""
    return int(height * 0.1)


def duration(length, cps):
    """按阅读速度定时长：字符数 / 每秒字符数。"""
    if cps <= 0:
        return 0
    return len(length) / cps if isinstance(length, str) else length / cps


def overlap(a_start, a_end, b_start):
    """重叠去重：b 的开始时间是否落在 a 的时间区间内。"""
    return a_start <= b_start < a_end


def anchor(value):
    """锚点归一化：统一到合法锚点名，非法值回退 center。"""
    if not isinstance(value, str):
        return "center"
    normalized = value.strip().lower()
    return normalized if normalized in _ANCHORS else "center"


def scale(size, height):
    """按分辨率缩放：以 1080p 为基准等比放大字号。"""
    return size * height / 1080


def export(text):
    """导出校验：真实换行转为字幕格式的硬换行标记 \\N，不残留字面量 \\n。"""
    return text.replace("\n", r"\N")


def language(text):
    """语言断行规则：含 CJK 字符按中文规则，否则按英文规则。"""
    for ch in text:
        if wide(ch) or "一" <= ch <= "鿿":
            return "zh"
    return "en"


def count(lines):
    """行数。"""
    return len(lines)


def clamp01(value):
    """归一钳制到 [0, 1]。"""
    return max(0.0, min(1.0, value))


def key(cue_id):
    """字幕键。"""
    return f"c:{cue_id}"
