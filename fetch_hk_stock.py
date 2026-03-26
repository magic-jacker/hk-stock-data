#!/usr/bin/env python3
import json
import os
from datetime import datetime
import requests

STOCKS = {
    '1211': {'name': '比亚迪股份'},
    '0700': {'name': '腾讯控股'},
    '3690': {'name': '美团'},
    '9988': {'name': '阿里巴巴'},
    '1810': {'name': '小米集团'},
}

def fetch_hk_stock_sina(code):
    try:
        url = f"https://hq.sinajs.cn/list=hk{code}"
        resp = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://finance.sina.com.cn/'
        }, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.text
        if 'hq_str_hk' not in data:
            return None
        parts = data.split('=')[1].strip('";').split(',')
        if len(parts) < 10:
            return None
        return {
            'code': code,
            'name': parts[0],
            'current': float(parts[6]) if parts[6] else 0,
            'last_close': float(parts[3]) if len(parts) > 3 and parts[3] else 0,
            'change': float(parts[7]) if len(parts) > 7 and parts[7] else 0,
            'change_pct': float(parts[8]) if len(parts) > 8 and parts[8] else 0,
            'volume': float(parts[11]) / 10000 if len(parts) > 11 and parts[11] else 0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    results = {}
    for code, info in STOCKS.items():
        data = fetch_hk_stock_sina(code)
        if data:
            results[code] = data
    output = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': results
    }
    os.makedirs('data', exist_ok=True)
    with open('data/hk_stock_latest.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    date_str = datetime.now().strftime('%Y%m%d')
    with open(f'data/hk_stock_{date_str}.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
