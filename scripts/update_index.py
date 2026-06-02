import json
import os
import re

# 生成された記事情報を読み込む
with open("article_entry.json", "r", encoding="utf-8") as f:
    raw = f.read().strip()
    # 最後の行のJSONだけ取得（printの出力が複数行の場合に対応）
    last_line = [l for l in raw.split("\n") if l.strip().startswith("{")][-1]
    entry = json.loads(last_line)

title = entry["title"]
file_path = entry["file"]
date = entry["date"]

# index.htmlを読み込む
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# すでに同じ記事が追加されていたらスキップ
if file_path in content:
    print(f"すでに追加済み: {title}")
else:
    new_item = f"""    <li>
      <a href="{file_path}">{title}</a>
      <p>{date}公開 ― {title}について詳しく解説します。</p>
    </li>"""

    content = re.sub(
        r'(<ul[^>]*id="articles"[^>]*>)',
        f'\\1\n{new_item}',
        content
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"index.html を更新しました: {title}")
