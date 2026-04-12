#!/bin/bash
# StockAI 服务健康监控与自动重启脚本
# 监控 URL
URL="http://192.168.2.102:3001/api/health"
LOG="/Users/here/.qclaw/workspace/memory/stockai_monitor.log"
PID_FILE="/Users/here/.qclaw/workspace/stockadvisor/stockadvisor.pid"
SERVER_DIR="/Users/here/.qclaw/workspace/stockadvisor"
MAX_RETRIES=3
RETRY_INTERVAL=10
# 记录函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

# 启动服务
start_service() {
    log "🚀 正在启动 StockAI 服务..."
    cd "$SERVER_DIR"
    nohup node server.js > /tmp/stockai_stdout.log 2>&1 &
    echo $! > "$PID_FILE"
    sleep 5
    
    # 等待服务启动
    for i in $(seq 1 10); do
        if curl -s -o /dev/null -w "%{http_code}" "$URL" --connect-timeout 5 | grep -q "200"; then
            log "✅ 服务启动成功！"
            return 0
        fi
        sleep 2
    done
    
    log "❌ 服务启动失败，请检查日志 /tmp/stockai_stdout.log"
    return 1
}

# 停止服务
stop_service() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            log "🛑 正在停止旧进程 (PID: $PID)..."
            kill "$PID" 2>/dev/null
            sleep 2
            # 强制终止
            if kill -0 "$PID" 2>/dev/null; then
                kill -9 "$PID" 2>/dev/null
            fi
        fi
        rm -f "$PID_FILE"
    fi
    
    # 确保端口已释放
    lsof -ti :3001 | xargs kill -9 2>/dev/null
}

# 健康检查
check_health() {
    local response
    local http_code
    
    response=$(curl -s -w "\n%{http_code}" "$URL" --connect-timeout 8 --max-time 15)
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "200" ]; then
        return 0
    else
        return 1
    fi
}

# 主程序
main() {
    log "========== 开始健康检查 =========="
    
    # 尝试健康检查
    for attempt in $(seq 1 $MAX_RETRIES); do
        if check_health; then
            log "✅ 服务正常响应 (HTTP 200)"
            log "========== 检查完成 =========="
            exit 0
        fi
        log "⚠️  第 $attempt/$MAX_RETRIES 次检查失败"
        if [ $attempt -lt $MAX_RETRIES ]; then
            sleep $RETRY_INTERVAL
        fi
    done
    
    # 所有检查都失败，执行重启
    log "🚨 服务无响应，开始执行重启流程..."
    
    # 检查进程是否真的死了
    if pgrep -f "node server.js" > /dev/null 2>&1; then
        log "⚠️  进程仍在运行但无响应，强制重启"
        stop_service
    fi
    
    # 等待端口释放
    sleep 3
    
    # 启动服务
    start_service
    
    # 最终验证
    if check_health; then
        log "🎉 重启成功！服务已恢复"
    else
        log "💥 重启后仍无法访问，通知人工干预"
    fi
    
    log "========== 检查完成 =========="
}

main "$@"
