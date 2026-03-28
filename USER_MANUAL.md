# 📈 StockAI 美股投顧助手 - 用戶操作手冊

> 版本：1.0 | 更新日期：2026-03-28

---

## 一、系統概述

StockAI 是一款 AI 驅動的美股投資顧問助手，整合即時股價、K線圖表、AI 分析與模擬交易功能，幫助投資者做出更明智的決策。

### 1.1 訪問地址

| 環境 | 地址 |
|------|------|
| 本機 | http://localhost:3001 |
| 區域網路 | http://192.168.2.72:3001 |

### 1.2 系統需求

- 現代瀏覽器（Chrome、Firefox、Safari、Edge）
- 建議使用手機或平板橫向瀏覽

---

## 二、功能介紹

### 2.1 即時股價查詢

**操作步驟：**
1. 在首頁搜尋框輸入美股代碼
2. 點擊「查詢」按鈕或按 Enter 鍵
3. 系統顯示股價資訊

**顯示內容：**
- 當前價格
- 漲跌金額 / 漲跌幅
- 開盤價 / 最高價 / 最低價
- 成交量
- 本益比 (P/E)
- 每股盈餘 (EPS)
- 市值
- 52 週高點 / 低點

**支援的熱門股票：**
```
AAPL  蘋果        MSFT  微軟
GOOGL Google     AMZN  亞馬遜
NVDA  輝達        META  Meta
TSLA  特斯拉      AMD   超微
NFLX  Netflix    BRK.B 波克夏
JPM   摩根大通    V     Visa
```

---

### 2.2 K 線圖表

**功能說明：**
- 顯示近 90 天的日 K 線圖
- 使用 TradingView Lightweight Charts
- 支援縮放、拖曳操作

**操作方式：**
- 滑鼠滾輪：縮放圖表
- 滑鼠拖曳：移動時間軸
- 觸控裝置：雙指縮放、單指拖曳

**注意：**
- K 線數據需要配置 Alpha Vantage API Key
- 未配置時顯示提示訊息

---

### 2.3 AI 深度分析

#### 分析模式一覽

| 模式 | 說明 | 適用場景 |
|------|------|----------|
| **全面分析** | 綜合分析公司各個面向 | 了解股票全貌 |
| **技術分析** | K線、均線、技術指標分析 | 短期操作決策 |
| **基本面分析** | 商業模式、財務、估值分析 | 長期投資評估 |
| **競爭對比** | 與同行業公司對比 | 選股決策 |
| **持倉分析** | 分析投資組合 | 資產配置優化 |
| **風險評估** | 全面風險評估 | 風險管理 |
| **買賣信號** | 具體買賣建議 | 執行交易 |
| **自由問答** | 任意問題 | 即時諮詢 |

#### 使用方式

1. 查詢股票後，點擊「AI 分析」按鈕
2. 選擇分析模式
3. 等待 AI 生成分析報告
4. 可繼續提問進行深入討論

#### 分析報告範例

```
【NVDA 全面分析報告】

1. 公司基本面
   輝達是全球 AI 晶片領導者...
   
2. 財務表現
   2024 營收成長 200%，毛利率 75%...
   
3. 估值分析
   目前本益比 65 倍，高於產業平均...
   
4. 技術面
   股價在 170-185 區間震盪...
   
5. 風險提示
   - 估值偏高風險
   - 競爭加劇風險
   
6. 投資建議
   建議：持有
   目標價：$195
   止損價：$160
```

---

### 2.4 模擬下單

#### 初始設定
- 初始資金：$100,000 美元
- 所有交易為模擬，不涉及真實資金

#### 買入股票
1. 查詢股票後，點擊「買入」按鈕
2. 輸入購買數量
3. 確認交易
4. 系統顯示交易結果

#### 賣出股票
1. 在持倉列表找到目標股票
2. 點擊「賣出」按鈕
3. 輸入賣出數量
4. 確認交易

#### 持倉管理
- 查看所有持倉股票
- 顯示成本價、當前價、盈虧
- 查看交易歷史記錄

#### 資金管理
- 查看可用現金
- 查看總資產（現金 + 持倉市值）
- 查看總盈虧

---

## 三、API 技術文檔

### 3.1 健康檢查

```http
GET /api/health
```

**回應：**
```json
{
  "status": "ok",
  "hasAPI": true,
  "model": "meta/llama-3.1-405b-instruct"
}
```

---

### 3.2 單股報價

```http
POST /api/quote
Content-Type: application/json

{
  "ticker": "NVDA"
}
```

**回應：**
```json
{
  "success": true,
  "ticker": "NVDA",
  "name": "NVIDIA Corp.",
  "price": 175.24,
  "change": -3.50,
  "changePercent": -1.96,
  "prevClose": 178.74,
  "high": 180.50,
  "low": 174.20,
  "volume": 45000000,
  "peRatio": 65.2,
  "eps": 2.69,
  "marketCap": 4320000000000,
  "source": "demo"
}
```

---

### 3.3 批量報價

```http
POST /api/quotes
Content-Type: application/json

{
  "tickers": ["AAPL", "MSFT", "NVDA"]
}
```

---

### 3.4 K 線數據

```http
GET /api/chart/NVDA
```

**回應：**
```json
{
  "success": true,
  "source": "alphavantage",
  "candles": [
    {
      "time": 1711238400,
      "open": 175.50,
      "high": 178.20,
      "low": 174.80,
      "close": 177.30,
      "volume": 45000000
    }
  ]
}
```

---

### 3.5 AI 分析

```http
POST /api/analyze
Content-Type: application/json

{
  "ticker": "NVDA",
  "type": "overview"
}
```

**分析類型：**
- `overview` - 全面分析
- `technical` - 技術分析
- `fundamental` - 基本面分析
- `compare` - 競爭對比
- `portfolio` - 持倉分析
- `risk` - 風險評估
- `signal` - 買賣信號
- `chat` - 自由問答

---

### 3.6 AI 問答

```http
POST /api/chat
Content-Type: application/json

{
  "messages": [
    { "role": "user", "content": "現在適合買入 NVDA 嗎？" }
  ]
}
```

---

## 四、常見問題

### Q1: 股價數據來源？
A: 優先使用 Alpha Vantage API 即時數據，若未配置則使用模擬數據。

### Q2: 如何配置即時數據？
A: 在 `.env` 文件中設置 `ALPHA_VANTAGE_KEY`，可至 https://www.alphavantage.co 免費申請。

### Q3: AI 分析準確嗎？
A: AI 分析僅供參考，不構成投資建議。投資決策請自行判斷。

### Q4: 模擬交易的數據會保存嗎？
A: 交易記錄保存在瀏覽器 localStorage 中，清除瀏覽器資料會重置。

### Q5: 支援哪些股票？
A: 支援所有美股上市公司，熱門股票有模擬數據備援。

---

## 五、風險聲明

⚠️ **重要聲明**

1. 本系統提供的所有資訊僅供參考，不構成投資建議
2. 股票投資有風險，可能導致本金虧損
3. 過往績效不代表未來表現
4. 投資前請諮詢專業人士
5. 模擬交易與實際交易存在差異

---

## 六、聯繫與支援

- **專案位置**：`/Users/here/.qclaw/workspace/stockadvisor`
- **GitHub**：https://github.com/wilson710808/family_pub
- **技術支援**：請在 GitHub 開 Issue

---

*本手冊最後更新：2026-03-28*
