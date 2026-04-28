import requests
import json
import re
from datetime import datetime, timezone, timedelta

# 北京时区
beijing_tz = timezone(timedelta(hours=8))
now = datetime.now(beijing_tz)
update_time = now.strftime("%Y-%m-%d %H:%M")

# 关键词过滤：只抓包含这些词的新闻
keywords = ['经济', '金融', '股市', 'A股', '央行', '通胀', 'GDP', '财政', '贸易', '政策',
            '外交', '国际', '总统', '选举', '制裁', '冲突', '关税', '债券', '汇率', '黄金',
            '石油', '贷款', '利率', '监管', '改革', '部长', '国务院', '白宫', '美联储',
            '人民币', '美元', '欧元', '能源', '芯片', '科技战', '供应链', '制造业']

def clean_text(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def is_relevant(title):
    for kw in keywords:
        if kw in title:
            return True
    return False

news_list = []

# 数据源1：新浪新闻热搜 (财经类)
try:
    resp = requests.get('https://api.news.sina.cn/feed/hotlist?type=finance', timeout=10)
    data = resp.json()
    for item in data.get('data', {}).get('hotList', [])[:20]:
        title = clean_text(item.get('title', ''))
        url = item.get('url', '')
        if is_relevant(title) and len(title) > 5:
            news_list.append({
                'title': title,
                'url': url,
                'source': '新浪财经',
                'hot': item.get('hotValue', ''),
                'time': ''
            })
except:
    pass

# 数据源2：百度热搜（通过非官方接口，过滤政治财经）
try:
    resp = requests.get('https://top.baidu.com/board?tab=realtime', timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    html = resp.text
    # 简单正则提取标题和链接
    matches = re.findall(r'<div class="c-single-text-ellipsis">(.*?)</div>.*?<a href="(.*?)"', html, re.DOTALL)
    for title, url in matches[:30]:
        title = clean_text(title)
        if is_relevant(title) and len(title) > 5:
            link = url if url.startswith('http') else 'https://top.baidu.com' + url
            news_list.append({
                'title': title,
                'url': link,
                'source': '百度热搜',
                'hot': '',
                'time': ''
            })
except:
    pass

# 去重（保留标题前20字比较）
seen = set()
unique_news = []
for item in news_list:
    short = item['title'][:20]
    if short not in seen:
        seen.add(short)
        unique_news.append(item)

top10 = unique_news[:10]

# 保存为 news.json
output = {
    'updateTime': update_time,
    'news': top10
}

with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ 更新完成，共 {len(top10)} 条新闻，时间 {update_time}")
