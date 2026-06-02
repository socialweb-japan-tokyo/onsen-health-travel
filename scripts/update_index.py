import json
import os
import re

# 生成された記事情報を読み込む
with open("article_entry.json", "r", encoding="utf-8") as f:
    entry = json.load(f)

title = entry["title"]
file_path = entry["file"]
date = entry["date"]

# index.htmlを読み込む
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 新しい記事のリストアイテムを作成
new_item = f"""    <li>
      <a href="{file_path}">{title}</a>
      <p>{date}公開 ― {title}について詳しく解説します。</p>
    </li>"""

# <ul id="articles"> の直後に挿入
content = re.sub(
    r'(<ul id="articles">)',
    f'\\1\n{new_item}',
    content
)

# index.htmlを保存
with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print(f"index.html を更新しました: {title}")
