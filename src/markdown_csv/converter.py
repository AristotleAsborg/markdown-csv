"""Markdown 表格 -> CSV 的核心逻辑，全部是纯函数，不碰文件系统。"""

from __future__ import annotations

import re

_SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")


def split_row(line: str) -> list[str]:
    """把一行 Markdown 表格拆成单元格列表，支持反斜杠加竖线的转义写法。"""
    text = line.strip()
    if text.startswith("|"):
        text = text[1:]
    if text.endswith("|") and not text.endswith("\\|"):
        text = text[:-1]

    cells: list[str] = []
    buf: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\\" and i + 1 < len(text) and text[i + 1] == "|":
            buf.append("|")
            i += 2
            continue
        if ch == "|":
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    return cells


def is_separator_row(line: str) -> bool:
    """判断一行是不是表头下面的分隔行，例如 ``| --- | :---: |``。"""
    cells = split_row(line)
    if not cells:
        return False
    return all(bool(cell) and _SEPARATOR_CELL.match(cell) for cell in cells)


def parse_rows(text: str) -> list[list[str]]:
    """提取文本里所有表格行，跳过空行、非表格行和分隔行。"""
    rows: list[list[str]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or "|" not in line:
            continue
        if is_separator_row(line):
            continue
        rows.append(split_row(line))
    return rows


def _format_cell(value: str, delimiter: str) -> str:
    if delimiter in value or '"' in value or "\n" in value or "\r" in value:
        return '"' + value.replace('"', '""') + '"'
    return value


def to_csv(text: str, *, delimiter: str = ",", include_header: bool = True) -> str:
    """把 Markdown 表格文本转成 CSV 文本（每行以 ``\n`` 结尾）。

    - ``delimiter``：字段分隔符，默认逗号。
    - ``include_header``：为 False 时丢掉第一行。
    - 输入里没有任何表格行时抛 ``ValueError``。
    """
    rows = parse_rows(text)
    if not rows:
        raise ValueError("输入里没有找到 Markdown 表格行")
    if not include_header:
        rows = rows[1:]
    lines = [delimiter.join(_format_cell(cell, delimiter) for cell in row) for row in rows]
    return "".join(line + "\n" for line in lines)
