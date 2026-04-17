#!/usr/bin/env python3
"""
實時股價爬蟲 - Twelve Data 主導備用方案
支持：實時股價 + K線數據
"""
import sys
import json
import urllib.request
import urllib.error
import ssl
import re
from datetime import datetime

def get_price_twelvedata(ticker):
    """Twelve Data 實時股價（免費 API）"""
    try:
        url = f"https://api.twelvedata.com/price?symbol={ticker}&apikey=demo"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read().decode())
        
        if 'price' in data:
            return {
                'ticker': ticker,
                'price': float(data['price']),
                'source': 'twelvedata'
            }
        return {'error': 'Twelve Data: 無價格數據'}
    except Exception as e:
        return {'error': f'Twelve Data error: {str(e)}'}

def get_quote_twelvedata(ticker):
    """Twelve Data 完整報價"""
    try:
        url = f"https://api.twelvedata.com/quote?symbol={ticker}&interval=1day&apikey=demo"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read().decode())
        
        if 'status' in data and data['status'] == 'error':
            return {'error': f"Twelve Data: {data.get('message', 'Unknown error')}"}
        
        return {
            'success': True,
            'ticker': ticker,
            'price': float(data.get('close', 0)),
            'change': float(data.get('percent_change_ytd', 0)),
            'changePercent': float(data.get('percent_change_ytd', 0)),
            'prevClose': float(data.get('previous_close', data.get('close', 0))),
            'open': float(data.get('open', 0)),
            'high': float(data.get('high', 0)),
            'low': float(data.get('low', 0)),
            'volume': int(data.get('volume', 0)),
            'timestamp': datetime.now().timestamp() * 1000,
            'source': 'twelvedata',
            'note': '實時數據 (Twelve Data)'
        }
    except Exception as e:
        return {'error': f'Twelve Data error: {str(e)}'}

def get_kline_twelvedata(ticker, days=90):
    """Twelve Data K線數據"""
    try:
        url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize={days}&format=JSON&apikey=demo"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            data = json.loads(response.read().decode())
        
        if 'status' in data and data['status'] == 'error':
            return {'success': False, 'error': f"Twelve Data K線: {data.get('message', 'Unknown')}"}
        
        values = data.get('values', [])
        candles = []
        for v in reversed(values):  # 從舊到新排列
            dt = datetime.strptime(v['datetime'], '%Y-%m-%d')
            ts = int(dt.timestamp())
            candles.append({
                'time': ts,
                'open': float(v['open']),
                'high': float(v['high']),
                'low': float(v['low']),
                'close': float(v['close']),
                'volume': int(v['volume']) if 'volume' in v else 0
            })
        
        return {
            'success': True,
            'ticker': ticker,
            'candles': candles,
            'source': 'twelvedata',
            'note': f'實時K線 ({len(candles)} 天)'
        }
    except Exception as e:
        return {'success': False, 'error': f'Twelve Data K線錯誤: {str(e)}'}

def get_quote_yahoo(ticker):
    """Yahoo Finance 完整報價（備用方案，無需 API Key）"""
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5d&interval=1d'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read().decode())
        
        result = data.get('chart', {}).get('result', [{}])[0]
        meta = result.get('meta', {})
        
        price = meta.get('regularMarketPrice', 0)
        prev = meta.get('previousClose', 0)
        change = price - prev if prev else 0
        change_pct = (change / prev * 100) if prev else 0
        
        return {
            'success': True,
            'ticker': ticker,
            'price': round(price, 2),
            'change': round(change, 2),
            'changePercent': round(change_pct, 2),
            'prevClose': round(prev, 2),
            'open': round(meta.get('regularMarketOpen', 0), 2),
            'high': round(meta.get('regularMarketDayHigh', 0), 2),
            'low': round(meta.get('regularMarketDayLow', 0), 2),
            'volume': meta.get('regularMarketVolume', 0),
            'timestamp': datetime.now().timestamp() * 1000,
            'source': 'yahoo',
            'note': 'Yahoo Finance 實時數據'
        }
    except Exception as e:
        return {'error': f'Yahoo error: {str(e)}'}

def get_kline_yahoo(ticker, days=90):
    """Yahoo Finance K線數據（備用方案，無需 API Key）"""
    try:
        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range={days}d&interval=1d'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            data = json.loads(response.read().decode())
        
        result = data.get('chart', {}).get('result', [{}])[0]
        ts = result.get('timestamp', [])
        q = result.get('indicators', {'quote': [{}]}).get('quote', [{}])[0]
        
        candles = []
        for i in range(len(ts)):
            if q.get('open', [None])[i] is not None:
                candles.append({
                    'time': ts[i],
                    'open': round(q['open'][i], 2),
                    'high': round(q['high'][i], 2),
                    'low': round(q['low'][i], 2),
                    'close': round(q['close'][i], 2),
                    'volume': q.get('volume', [0])[i] or 0
                })
        
        return {
            'success': True,
            'ticker': ticker,
            'candles': candles,
            'source': 'yahoo',
            'note': f'Yahoo Finance K線 ({len(candles)} 天)'
        }
    except Exception as e:
        return {'success': False, 'error': f'Yahoo K線錯誤: {str(e)}'}

# 備用：模擬數據（當 API 失敗時）
def get_simulated_data(ticker):
    """備用模擬數據"""
    import random
    base_price = 200.0
    return {
        'ticker': ticker,
        'name': ticker,
        'price': round(base_price + random.uniform(-20, 20), 2),
        'change': round(random.uniform(-5, 5), 2),
        'changePercent': round(random.uniform(-2, 2), 2),
        'prevClose': round(base_price + random.uniform(-5, 5), 2),
        'open': round(base_price + random.uniform(-3, 3), 2),
        'high': round(base_price + random.uniform(5, 15), 2),
        'low': round(base_price + random.uniform(-15, -5), 2),
        'volume': random.randint(10000000, 100000000),
        'peRatio': round(random.uniform(15, 35), 1),
        'eps': round(random.uniform(5, 15), 2),
        'marketCap': random.randint(1000000000000, 3000000000000),
        'fiftyTwoWeekHigh': round(base_price + 30, 2),
        'fiftyTwoWeekLow': round(base_price - 50, 2),
        'timestamp': datetime.now().timestamp() * 1000,
        'source': 'simulated',
        'note': '模擬數據'
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': '請提供股票代碼'}))
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    
    if '--kline' in sys.argv:
        result = get_kline_twelvedata(ticker)
        # Twelve Data 失敗時，改用 Yahoo Finance
        if not result.get('success'):
            result = get_kline_yahoo(ticker)
    else:
        result = get_quote_twelvedata(ticker)
        # Twelve Data 失敗時，改用 Yahoo Finance
        if 'error' in result:
            yahoo_result = get_quote_yahoo(ticker)
            if 'success' in yahoo_result:
                result = yahoo_result
            else:
                result = get_simulated_data(ticker)
    
    print(json.dumps(result))
