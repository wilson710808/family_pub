# StockAI - 美股 AI 投顧助手

一個專業的美股分析網站，結合 AI 技術提供投資建議。

## ✨ 功能特色

- 📊 **即時股價** - 顯示主要股票的實時價格
- 🔍 **全面分析** - AI 生成的股票分析報告
- 📈 **技術面分析** - K線、均線、RSI、MACD
- 💰 **基本面分析** - 財務、估值、競爭力
- ⚠️ **風險評估** - 估值、風險、黑天鵝
- 🎯 **買賣信號** - 具體的買入/賣出建議
- 💼 **持倉追蹤** - 虛擬投資組合
- ⭐ **自選股** - 關注的股票列表
- 💬 **智能問答** - 隨時提問投資相關問題

## 🚀 快速開始

### 1. 安裝

```bash
npm install
```

### 2. 配置

```bash
cp .env.example .env
```

編輯 `.env` 填入你的 API Key：

```bash
# NVIDIA NIM API (免費)
OPENAI_API_KEY=nvapi-xxxxx
OPENAI_BASE_URL=https://integrate.api.nvidia.com/v1
OPENAI_MODEL=meta/llama-3.1-405b-instruct
```

### 3. 啟動

```bash
npm start
```

訪問 http://localhost:3001

## ⚙️ 配置

### 環境變量

| 變量 | 說明 | 預設值 |
|------|------|--------|
| OPENAI_API_KEY | API Key | - |
| OPENAI_BASE_URL | API 端點 | NVIDIA NIM |
| OPENAI_MODEL | 模型 | llama-3.1-405b |
| PORT | 端口 | 3001 |

## 🔒 安全說明

- API Key 存儲在 `.env`，不會提交到 Git
- `.env` 已加入 `.gitignore`

## 📁 目錄結構

```
stockadvisor/
├── public/
│   └── index.html      # 前端頁面
├── server.js           # 後端服務
├── stock_price.py      # 股價爬蟲
├── package.json
└── .env.example
```

## License

MIT
