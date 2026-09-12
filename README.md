# markdown-csv

把 Markdown 表格转换成 CSV 的小工具，提供命令行入口和 Python API。

- 输入：标准 Markdown 管道表格（可带 `:---` 对齐标记，也可省略首尾的 `|`）
- 输出：CSV 文本，含逗号 / 双引号 / 换行的单元格会自动加引号

## 安装

```bash
python -m pip install -e ".[dev]"
```

发布到 PyPI 后可以 `pip install markdown-csv`。

## 命令行用法

```bash
markdown-csv table.md                  # 转换后写到标准输出
markdown-csv table.md -o table.csv     # 写到文件
cat table.md | markdown-csv -          # 从标准输入读取
markdown-csv table.md -d ';'           # 换成别的分隔符
markdown-csv table.md --no-header      # 丢掉表头行
```

输入里没有表格行时，CLI 会把错误打印到 stderr 并返回退出码 `1`。

## Python API

```python
from markdown_csv import to_csv

text = "| a | b |\n| --- | --- |\n| 1 | 2 |\n"
to_csv(text)
# 'a,b\n1,2\n'
```

其它可用的纯函数：`split_row(line)`、`is_separator_row(line)`、`parse_rows(text)`。

## 行为说明

- 分隔行（如 `| --- | :---: |`）会被跳过，不会出现在 CSV 里。
- 单元格里的竖线用 `\|` 转义。
- 含分隔符、双引号或换行的单元格会用双引号包裹，内部的 `"` 写成 `""`。
- 输入里没有任何表格行时 `to_csv` 抛 `ValueError`。

## 开发与测试

```bash
python -m pytest -q
python -m ruff check .
python scripts/check_blacklist.py
```

测试不依赖系统临时目录：需要落盘的 CLI 端到端用例在仓库根目录建 `.scratch/`，并在用例结束时删除。
