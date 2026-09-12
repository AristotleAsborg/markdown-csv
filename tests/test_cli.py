"""CLI 端到端测试。落盘文件放在项目内的 .scratch/，用例结束删掉。"""

import shutil
from pathlib import Path

from markdown_csv.cli import main

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_cli_writes_output_file() -> None:
    scratch = REPO_ROOT / ".scratch"
    scratch.mkdir(exist_ok=True)
    src = scratch / "table.md"
    dst = scratch / "table.csv"
    try:
        src.write_text("| a | b |\n| --- | --- |\n| 1 | 2 |\n", encoding="utf-8")
        assert main([str(src), "-o", str(dst)]) == 0
        assert dst.read_text(encoding="utf-8") == "a,b\n1,2\n"
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def test_cli_returns_1_when_input_has_no_table(capsys) -> None:
    scratch = REPO_ROOT / ".scratch"
    scratch.mkdir(exist_ok=True)
    src = scratch / "plain.md"
    try:
        src.write_text("没有表格\n", encoding="utf-8")
        assert main([str(src)]) == 1
        captured = capsys.readouterr()
        assert "错误" in captured.err
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
