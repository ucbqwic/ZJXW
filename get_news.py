import requests
import json
from datetime import datetime

def get_baidu_hot():
    # 百度热搜实时榜 API（需添加 User-Agent）
    url = "https://top.baidu.com/api/board?tab=realtime&platform=wise"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        cards = data.get("data", {}).get("cards", [])
        news_list = []
        for card in cards:
            content = card.get("content", [])
            for item in content:
                title = item.get("word", "")
                url = item.get("url", "")
                hot_score = item.get("hotScore", 0)
                if title:
                    news_list.append({
                        "title": title,
                        "url": url if url else f"https://www.baidu.com/s?wd={title}",
                        "source": "百度热搜",
                        "hot": hot_score,
                        "time": datetime.now().strftime("%H:%M")
                    })
        return news_list[:30]  # 取前30条
    except Exception as e:
        print("抓取百度热搜失败:", e)
        return []

if
