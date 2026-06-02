import json
import os
import re

with open("article_entry.json", "r", encoding="utf-8") as f:
    raw = f.read().strip()
    last_line = [l for l in raw.split("\n") if l.strip().startswith("{")][-1]
    entry = json.loads(last_line)

title = entry["title"]
file_path = entry["file"]
date = entry["date"]

# サムネイルの背景色をローテーション
colors = [
    "linear-gradient(135deg,#1a4a40 0%,#2d7a60 50%,#4aaa85 100%)",
    "linear-gradient(135deg,#2d3a4a 0%,#4a6a7a 50%,#7aaaba 100%)",
    "linear-gradient(135deg,#4a3a2a 0%,#7a5a40 50%,#aa8a65 100%)",
    "linear-gradient(135deg,#3a2a4a 0%,#6a4a7a 50%,#9a7aaa 100%)",
    "linear-gradient(135deg,#1a3a2a 0%,#2a5a4a 50%,#3a7a6a 100%)",
    "linear-gradient(135deg,#4a3a1a 0%,#7a6a3a 50%,#aa9a5a 100%)",
]

# 既存の記事数を数えて色を決める
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

count = content.count('class="card"')
color = colors[count % len(colors)]

if file_path in content:
    print(f"すでに追加済み: {title}")
else:
    new_card = f"""      <a class="card" href="{file_path}">
        <div class="card-thumb" style="background:{color}">
          <div class="thumb-label">Onsen Guide</div>
        </div>
        <div class="card-body">
          <div class="card-tag">温泉・健康</div>
          <div class="card-title">{title}</div>
          <div class="card-date">{date}</div>
        </div>
      </a>"""

    content = re.sub(
        r'(<div class="grid" id="articles">)',
        f'\\1\n{new_card}',
        content
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"index.html を更新しました: {title}")
