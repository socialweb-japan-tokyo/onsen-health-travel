import anthropic
import os
import datetime
import json

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# 記事テーマのリスト
themes = [
    "草津温泉と関節炎・リウマチへの効果",
    "箱根温泉の美肌効果と皮膚疾患への働き",
    "別府温泉の泥湯と慢性疲労への効果",
    "有馬温泉の金泉・銀泉と神経痛への効果",
    "登別温泉の硫黄泉とアトピー性皮膚炎",
    "指宿温泉の砂むし湯と腰痛・冷え性改善",
    "玉造温泉と婦人科系疾患への温泉療法",
    "下呂温泉のアルカリ性単純温泉と筋肉痛",
]

# 今週のテーマを日付ベースで選ぶ
week_number = datetime.date.today().isocalendar()[1]
theme = themes[week_number % len(themes)]

# Claude APIで記事生成
message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=2000,
    messages=[
        {
            "role": "user",
            "content": f"""以下のテーマで、温泉・医療ツーリズムの情報記事をHTML形式で書いてください。

テーマ：{theme}

条件：
- 文字数は800〜1200字程度
- 見出し（h2）を3つ使う
- 具体的な効能・アクセス・おすすめ滞在期間を含める
- <article>タグで全体を囲む
- bodyタグやhtmlタグは不要、articleタグの中身だけ出力
- 読者は健康に関心がある30〜60代の日本人"""
        }
    ]
)

article_content = message.content[0].text
today = datetime.date.today().strftime("%Y-%m-%d")
filename = f"articles/{today}-{week_number}.html"

# HTMLファイルとして保存
html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{theme} | 温泉・医療ツーリズムガイド</title>
  <style>
    body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
    h1, h2 {{ color: #2c7a7b; }}
    a {{ color: #2c7a7b; }}
    .back {{ margin-bottom: 20px; }}
  </style>
</head>
<body>
  <div class="back"><a href="../index.html">← トップに戻る</a></div>
  <h1>{theme}</h1>
  {article_content}
  <p><small>公開日：{today}</small></p>
</body>
</html>"""

os.makedirs("articles", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    f.write(html)

# index.htmlに記事リンクを追加するためのデータ保存
entry = {"title": theme, "file": filename, "date": today}
print(json.dumps(entry, ensure_ascii=False))
