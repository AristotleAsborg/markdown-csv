"""命令行入口：markdown-csv input.md -o output.csv"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from markdown_csv.converter import to_csv


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="markdown-csv",
        description="把 Markdown 表格转换成 CSV。",
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="-",
        help="待转换的 Markdown 文件，'-' 或省略表示从标准输入读取",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="-",
        help="输出文件，'-' 或省略表示写到标准输出",
    )
    parser.add_argument(
        "-d",
        "--delimiter",
        default=",",
        help="字段分隔符，默认是逗号",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="丢掉第一行表头",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.input in (None, "-"):
        text = sys.stdin.read()
    else:
        text = Path(args.input).read_text(encoding="utf-8")

    try:
        csv_text = to_csv(text, delimiter=args.delimiter, include_header=not args.no_header)
    except ValueError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    if args.output in (None, "-"):
        sys.stdout.write(csv_text)
    else:
        Path(args.output).write_text(csv_text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
