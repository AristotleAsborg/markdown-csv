"""converter 模块的单元测试：导入 + 正例 + 边界/反例。"""

import pytest

import markdown_csv
from markdown_csv import to_csv
from markdown_csv.converter import is_separator_row, parse_rows, split_row


def test_package_is_importable() -> None:
    assert markdown_csv.__version__ == "0.1.0"
    assert callable(markdown_csv.to_csv)


def test_to_csv_basic_table() -> None:
    text = "| name | age |\n| --- | --- |\n| alice | 30 |\n| bob | 25 |\n"
    assert to_csv(text) == "name,age\nalice,30\nbob,25\n"


def test_to_csv_quotes_cells_containing_delimiter() -> None:
    text = "| a | b |\n| --- | --- |\n| x,y | z |\n"
    assert to_csv(text) == 'a,b\n"x,y",z\n'


def test_escaped_pipe_stays_inside_cell() -> None:
    text = "| a | b |\n| --- | --- |\n| 1 \\| 2 | 3 |\n"
    assert to_csv(text) == "a,b\n1 | 2,3\n"


def test_alignment_separator_and_missing_outer_pipes() -> None:
    text = "name | age\n:--- | ---:\ncarol | 41\n"
    assert to_csv(text) == "name,age\ncarol,41\n"


def test_parse_rows_ignores_non_table_lines() -> None:
    text = "标题\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n"
    assert parse_rows(text) == [["a", "b"], ["1", "2"]]


def test_split_row_keeps_empty_cells() -> None:
    assert split_row("| a |  | c |") == ["a", "", "c"]


def test_is_separator_row_detects_alignment_row() -> None:
    assert is_separator_row("| --- | :---: |")
    assert not is_separator_row("| a | --- |")


def test_custom_delimiter_and_no_header() -> None:
    text = "| a | b |\n| --- | --- |\n| 1 | 2 |\n"
    assert to_csv(text, delimiter=";") == "a;b\n1;2\n"
    assert to_csv(text, include_header=False) == "1,2\n"


def test_to_csv_raises_without_table() -> None:
    with pytest.raises(ValueError):
        to_csv("这里没有任何表格\n\n普通段落。\n")
