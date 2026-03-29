#!/usr/bin/env python3
"""
实时股价爬虫 - 多数据源备用方案
支持：实时股价 + K线数据
"""
import sys
import json
import urllib.request
import urllib.error
import ssl
import re

def get_price_yahoo(ticker):
    """Yahoo Finance Query API"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read().decode())
            
        result = data['chart']['result'][0]
        meta = result['meta']
        
        price = meta.get('regularMarketPrice')
        prevClose = meta.get('previousClose', meta.get('chartPreviousClose', price))
        
        if not price:
            return {'error': 'Yahoo: 无法获取价格'}
        
        change = price - prevClose if prevClose else 0
        changePercent = (change / prevClose * 100) if prevClose else 0
        
        return {
            'ticker': ticker,
            'price': price,
            'change': round(change, 2),
            'changePercent': round(changePercent, 2),
            'prevClose': prevClose,
            'open': meta.get('chartPreviousClose', price),
            'high': price * 1.01,
            'low': price * 0.99,
            'source': 'yahoo'
        }
    except Exception as e:
        return {'error': f'Yahoo error: {str(e)}'}

def get_price_google(ticker):
    """Google Finance 网页爬虫"""
    try:
        url = f"https://www.google.com/finance/quote/{ticker}:NASDAQ"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            html = response.read().decode()
        
        price_match = re.search(r'class="fxKbKd"[^>]*>([\d,.]+)<', html)
        if not price_match:
            price_match = re.search(r'data-last-price="([\d,.]+)"', html)
        
        if price_match:
            price = float(price_match.group(1).replace(',', ''))
            return {
                'ticker': ticker,
                'price': price,
                'source': 'google'
            }
        return {'error': 'Google: 无法解析价格'}
    except Exception as e:
        return {'error': f'Google error: {str(e)}'}

def get_realtime_price(ticker):
    """尝试多个数据源获取实时股价"""
    sources = [
        ('Yahoo Finance', get_price_yahoo),
        ('Google Finance', get_price_google),
    ]
    
    for name, func in sources:
        result = func(ticker)
        if 'price' in result and result['price']:
            result['note'] = f'实时数据 ({name})'
            return result
    
    return {'error': '所有数据源都无法获取价格'}

def get_kline_yahoo(ticker, days=90):
    """Yahoo Finance K线数据"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range={days}d"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read().decode())
        
        result = data['chart']['result'][0]
        timestamps = result.get('timestamp', [])
        quote = result.get('indicators', {}).get('quote', [{}])[0]
        
        candles = []
        for i, ts in enumerate(timestamps):
            if ts and i < len(quote.get('open', [])) and quote['open'][i] is not None:
                candles.append({
                    'time': ts,
                    'open': quote['open'][i],
                    'high': quote['high'][i],
                    'low': quote['low'][i],
                    'close': quote['close'][i],
                    'volume': quote['volume'][i] if i < len(quote.get('volume', [])) else 0
                })
        
        return {
            'success': True,
            'ticker': ticker,
            'candles': candles,
            'source': 'yahoo',
            'note': f'實時K線 ({len(candles)} 天)'
        }
    except Exception as e:
        return {'success': False, 'error': f'Yahoo K线错误: {str(e)}'}

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供股票代码'}))
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    
    if '--kline' in sys.argv:
        result = get_kline_yahoo(ticker)
    else:
        result = get_realtime_price(ticker)
    
    print(json.dumps(result))
