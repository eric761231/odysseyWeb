import os
import json

# 修正路徑，確保 articles.json 產生在 html/articles/
ARTICLES_ROOT = os.path.abspath(os.path.dirname(__file__))
months = [f'2025-{str(m).zfill(2)}' for m in range(4, 11)]
articles_json = {}

for month in months:
    folder = os.path.join(ARTICLES_ROOT, month)
    month_articles = []
    if os.path.isdir(folder):
        for fname in sorted(os.listdir(folder)):
            if fname.endswith('.txt'):
                fpath = os.path.join(folder, fname)
                try:
                    with open(fpath, encoding='utf-8') as f:
                        content = f.read()
                    month_articles.append({
                        'file': fname,
                        'date': fname[:8],
                        'content': content
                    })
                except Exception as e:
                    month_articles.append({
                        'file': fname,
                        'date': fname[:8],
                        'content': f'讀取失敗: {e}'
                    })
    articles_json[month] = month_articles


# articles.json 產生在 html/articles/
with open(os.path.join(ARTICLES_ROOT, 'articles.json'), 'w', encoding='utf-8') as f:
    json.dump(articles_json, f, ensure_ascii=False, indent=2)

print('已產生 articles.json')
