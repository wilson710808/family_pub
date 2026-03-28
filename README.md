# 📈 StockAI - 美股 AI 投顧助手

> 智能美股投資顧問，整合即時股價、K線圖表、AI 深度分析與模擬交易

[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ✨ 功能特色

| 功能 | 說明 |
|------|------|
| 📊 **即時股價** | 輸入美股代碼，立即查詢股價、漲跌幅、成交量等 |
| 📈 **K 線圖表** | TradingView 專業級圖表，支援縮放拖曳 |
| 🤖 **AI 深度分析** | 8 種分析模式：全面、技術、基本面、風險評估等 |
| 💬 **AI 問答** | 與 AI 投顧顧問即時對話 |
| 💰 **模擬下單** | $10 萬美元虛擬資金，練習投資策略 |

---

## 🚀 快速開始

### 1. 安裝依賴

```bash
git clone https://github.com/wilson710808/family_pub.git
cd family_pub
npm install
```

### 2. 配置環境變數

建立 `.env` 文件：

```env
# AI API (NVIDIA NIM)
OPENAI_API_KEY=nvapi-xxx
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
OPENAI_MODEL=meta/llama-3.1-405b-instruct

# 股價 API (選填，免費申請: https://www.alphavantage.co)
ALPHA_VANTAGE_KEY=your-key-here

# 服務端口
PORT=3001
```

### 3. 啟動服務

```bash
node server.js
```

### 4. 訪問應用

- 本機：http://localhost:3001
- 區域網路：http://你的IP:3001

---

## 📖 使用指南

### 查詢股價

1. 在搜尋框輸入股票代碼（如 `NVDA`、`AAPL`）
2. 點擊「查詢」或按 Enter
3. 查看即時股價資訊

### AI 分析模式

| 模式 | 說明 | 適用場景 |
|------|------|----------|
| 全面分析 | 公司基本面 + 財務 + 技術 + 投資建議 | 了解股票全貌 |
| 技術分析 | 趨勢、支撐壓力、技術指標 | 短期操作 |
| 基本面分析 | 商業模式、財務健康、估值 | 長期投資 |
| 競爭對比 | 與同行業公司對比 | 選股決策 |
| 風險評估 | 估值/業務/競爭/宏觀風險 | 風險管理 |
| 買賣信號 | 具體買入價、止損價、目標價 | 執行交易 |

### 模擬下單

- 初始資金：$100,000 美元
- 支援買入、賣出、部分賣出
- 交易記錄自動保存（localStorage）

---

## 🔧 API 文檔

### 健康檢查

```http
GET /api/health
```

### 單股報價

```http
POST /api/quote
Content-Type: application/json

{ "ticker": "NVDA" }
```

### K 線數據

```http
GET /api/chart/:ticker
```

### AI 分析

```http
POST /api/analyze
Content-Type: application/json

{ 
  "ticker": "NVDA",
  "type": "overview"  // overview|technical|fundamental|risk|signal
}
```

### AI 問答

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

## 📁 專案結構

```
stockadvisor/
├── server.js           # 後端服務 (Express)
├── public/
│   └── index.html      # 前端 SPA
├── stock_price.py      # 股價爬蟲 (備用)
├── USER_MANUAL.md      # 用戶操作手冊
├── package.json
├── .env.example
└── .gitignore
```

---

## 🔑 API Key 申請

### NVIDIA NIM API (AI 分析)

1. 訪問 https://build.nvidia.com
2. 註冊並獲取 API Key
3. 選擇模型：`meta/llama-3.1-405b-instruct`

### Alpha Vantage (即時股價)

1. 訪問 https://www.alphavantage.co/support/#api-key
2. 免費申請 API Key
3. 每日 500 次免費調用

---

## ⚠️ 風險聲明

1. 本系統所有資訊僅供參考，不構成投資建議
2. 股票投資有風險，可能導致本金虧損
3. 過往績效不代表未來表現
4. 投資前請諮詢專業人士

---

## 📄 授權

MIT License

---

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

*最後更新：2026-03-28*
