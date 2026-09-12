"""扫描仓库里是否出现了被禁止的 API（例如系统临时目录相关用法）。

用法：python scripts/check_blacklist.py
退出码 0 表示通过，1 表示发现违规。
"""

from __future__ import annotations

import sys
from pathlib import Path

FORBIDDEN = ("tmp_path", "tmpdir", "temp" + "file", "TemporaryDirectory")
ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
SKIP_DIRS = {".git", ".scratch", ".venv", "build", "dist", "__pycache__", ".ruff_cache"}


def iter_python_files() -> list[Path]:
    found: list[Path] = []
    for path in sorted(ROOT.rglob("*.py")):
        if path.resolve() == SELF:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        found.append(path)
    return found


def main() -> int:
    problems: list[str] = []
    for path in iter_python_files():
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for token in FORBIDDEN:
                if token in line:
                    rel = path.relative_to(ROOT)
                    problems.append(f"{rel}:{lineno}: 禁止使用 {token!r}")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        print(f"发现 {len(problems)} 处禁止用法", file=sys.stderr)
        return 1

    print("blacklist 检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
