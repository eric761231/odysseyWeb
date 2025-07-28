
import os
import json
import time


def generate_articles_json():
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
    with open(os.path.join(ARTICLES_ROOT, 'articles.json'), 'w', encoding='utf-8') as f:
        json.dump(articles_json, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    print('自動監控啟動，每秒更新 articles.json，Ctrl+C 可中斷')
    last_files = set()
    while True:
        # 收集所有 txt 檔案檔名
        current_files = set()
        ARTICLES_ROOT = os.path.abspath(os.path.dirname(__file__))
        months = [f'2025-{str(m).zfill(2)}' for m in range(4, 11)]
        for month in months:
            folder = os.path.join(ARTICLES_ROOT, month)
            if os.path.isdir(folder):
                for fname in os.listdir(folder):
                    if fname.endswith('.txt'):
                        current_files.add(f'{month}/{fname}')
        if current_files != last_files:
            generate_articles_json()
            print(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] 已產生 articles.json')
            last_files = current_files
        time.sleep(1)
