#!/usr/bin/env python3
"""
美股即時股價爬蟲 - 使用標準庫
"""

import json
import sys
import urllib.request
import urllib.parse
from typing import Dict, Optional

def get_stock_price(ticker: str) -> Optional[Dict]:
    """獲取單支股票價格"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": "5d",
            "events": "history"
        }
        
        full_url = url + "?" + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(
            full_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        result = data.get("chart", {}).get("result", [])
        
        if not result:
            return None
            
        meta = result[0].get("meta", {})
        quote = result[0].get("indicators", {}).get("quote", [{}])[0]
        
        price = meta.get("regularMarketPrice")
        if price is None:
            return None
            
        prev_close = meta.get("chartPreviousClose") or meta.get("previousClose") or meta.get("regularMarketPreviousClose")
        
        return {
            "ticker": ticker.upper(),
            "name": meta.get("shortName") or meta.get("longName") or ticker,
            "price": price,
            "change": meta.get("regularMarketChange") or 0,
            "changePercent": meta.get("regularMarketChangePercent") or 0,
            "prevClose": prev_close if prev_close else price,
            "open": meta.get("regularMarketOpen") or quote.get("open", [None])[-1] or price,
            "high": meta.get("regularMarketDayHigh") or quote.get("high", [None])[-1] or price,
            "low": meta.get("regularMarketDayLow") or quote.get("low", [None])[-1] or price,
            "volume": meta.get("regularMarketVolume") or 0,
            "peRatio": meta.get("trailingPE") or 0,
            "eps": meta.get("epsTrailingTwelveMonths") or 0,
            "marketCap": meta.get("marketCap") or 0,
            "fiftyTwoWeekHigh": meta.get("fiftyTwoWeekHigh") or 0,
            "fiftyTwoWeekLow": meta.get("fiftyTwoWeekLow") or 0,
            "timestamp": (meta.get("regularMarketTime") or 0) * 1000,
            "source": "yahoo"
        }
        
    except Exception as e:
        print(f"Error for {ticker}: {e}", file=sys.stderr)
        return None


def get_multiple_prices(tickers: list) -> list:
    """獲取多支股票價格"""
    results = []
    for t in tickers:
        result = get_stock_price(t)
        if result:
            results.append(result)
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
        result = get_stock_price(ticker)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps({"error": f"Failed to get {ticker}"}))
    else:
        tickers = ["NVDA", "AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "META", "AMD"]
        results = get_multiple_prices(tickers)
        print(json.dumps(results, indent=2))
