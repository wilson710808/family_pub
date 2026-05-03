# Release Notes

## v2.0.0 (2026-05-03)
### 🏗️ 架構升級
- **AI Gateway 整合** — 所有 AI 請求（分析 + 問答）改透過 AI Gateway 轉發
  - 移除直接呼叫 NVIDIA API 的 `proxyFetch`（CONNECT 代理隧道）
  - 移除 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL` 依賴
  - 移除多模型降級邏輯，改由 Gateway 統一管理 API Key 池化 + 速率限制 + 負載均衡
- **Webspace #07 部署** — 遷入多網站工作區架構
  - 端口 3007，Nginx 反代路徑 `/ws/07-stock-ai/`
  - systemd 服務 `webspace-07-stock-ai.service`（開機自啟）
  - 監聽地址改為 `127.0.0.1`（僅 Nginx 可訪問）

### 📦 新增環境變數
- `GATEWAY_URL` — AI Gateway 服務地址（預設 `http://127.0.0.1:3005`）
- `GATEWAY_API_PATH` — Gateway API 路徑（預設 `/api/query`）
- `APP_ID` — 在 Gateway 註冊的應用 ID（預設 `stock-ai`）

### 🗑️ 移除
- `proxyFetch` HTTP CONNECT 代理隧道（不再需要繞 VPN）
- `net`/`tls` 模組依賴
- `config.apiKey`、`config.baseUrl`、`config.fallbackModels`

## v1.0.0 (2026-03-25)
### ✨ New Features
- **即時股價** - 顯示股票實時報價
- **AI 分析** - 多種分析模式（全面、技術、基本面、風險、買賣信號）
- **自選股** - 追蹤關注的股票
- **持倉追蹤** - 虛擬投資組合
- **智能問答** - AI 投顧回答問題
- **逐步反饋** - 分析過程實時顯示

### 🔧 Technical
- 使用 NVIDIA NIM API（免費額度）
- Python 爬蟲獲取股價
- 手機優先響應式設計

### 🛡️ Security
- API Key 不暴露
- CORS 可配置
