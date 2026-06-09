# CC Switch 数据库结构

## 概述

CC Switch 使用 SQLite 数据库存储所有配置。数据库文件位于 `~/.cc-switch/cc-switch.db`。

## 支持的平台

| 平台 | app_type | 说明 |
|------|----------|------|
| Claude Code | claude | Anthropic Claude |
| Codex | codex | OpenAI Codex |
| Gemini CLI | gemini | Google Gemini |
| OpenCode | opencode | OpenCode |
| Hermes | hermes | Hermes |

## 表结构

### providers

存储 AI Agent 平台的 Provider 配置。

| 列名 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 主键 |
| app_type | TEXT | 平台类型：claude, codex, gemini, opencode, hermes |
| name | TEXT | 显示名称 |
| settings_config | TEXT | JSON 格式的完整配置 |
| website_url | TEXT | 网站地址 |
| category | TEXT | 分类：official, cn_official, aggregator |
| provider_type | TEXT | Provider 类型：xiaomimimo, zhipu, nvidia 等 |
| is_current | BOOLEAN | 是否当前使用 |
| in_failover_queue | BOOLEAN | 是否在故障转移队列 |
| cost_multiplier | TEXT | 成本倍数 |
| limit_daily_usd | TEXT | 每日限额（美元） |
| limit_monthly_usd | TEXT | 每月限额（美元） |
| created_at | INTEGER | 创建时间戳 |
| sort_index | INTEGER | 排序索引 |
| notes | TEXT | 备注 |
| icon | TEXT | 图标 |
| icon_color | TEXT | 图标颜色 |
| meta | TEXT | 元数据 JSON |

#### settings_config 示例

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-xxx",
    "ANTHROPIC_BASE_URL": "https://api.example.com/v1",
    "ANTHROPIC_MODEL": "model-name",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "haiku-model",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "sonnet-model",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "opus-model"
  },
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...]
  },
  "enabledPlugins": {...},
  "language": "中文",
  "theme": "dark"
}
```

### mcp_servers

存储 MCP 服务器配置。

| 列名 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 主键 |
| name | TEXT | 名称 |
| server_config | TEXT | JSON 格式的服务器配置 |
| description | TEXT | 描述 |
| homepage | TEXT | 主页 |
| docs | TEXT | 文档链接 |
| tags | TEXT | 标签 JSON 数组 |
| enabled_claude | BOOLEAN | 是否在 Claude 中启用 |
| enabled_codex | BOOLEAN | 是否在 Codex 中启用 |
| enabled_gemini | BOOLEAN | 是否在 Gemini 中启用 |
| enabled_opencode | BOOLEAN | 是否在 OpenCode 中启用 |
| enabled_hermes | BOOLEAN | 是否在 Hermes 中启用 |

#### server_config 示例

**stdio 类型（npm 包）：**
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@scope/package"]
}
```

**stdio 类型（本地命令）：**
```json
{
  "type": "stdio",
  "command": "command-name",
  "args": ["arg1", "arg2"]
}
```

**http 类型：**
```json
{
  "type": "http",
  "url": "https://example.com/mcp",
  "headers": {
    "Authorization": "Bearer xxx"
  }
}
```

### skills

存储技能配置。

| 列名 | 类型 | 说明 |
|------|------|------|
| id | TEXT | 主键 |
| name | TEXT | 名称 |
| description | TEXT | 描述 |
| directory | TEXT | 目录路径 |
| repo_owner | TEXT | 仓库所有者 |
| repo_name | TEXT | 仓库名称 |
| repo_branch | TEXT | 仓库分支 |
| readme_url | TEXT | README 链接 |
| enabled_claude | BOOLEAN | 是否在 Claude 中启用 |
| enabled_codex | BOOLEAN | 是否在 Codex 中启用 |
| enabled_gemini | BOOLEAN | 是否在 Gemini 中启用 |
| enabled_opencode | BOOLEAN | 是否在 OpenCode 中启用 |
| enabled_hermes | BOOLEAN | 是否在 Hermes 中启用 |
| installed_at | INTEGER | 安装时间戳 |
| content_hash | TEXT | 内容哈希 |
| updated_at | INTEGER | 更新时间戳 |

### settings

存储应用设置。

| 列名 | 类型 | 说明 |
|------|------|------|
| key | TEXT | 主键 |
| value | TEXT | 值 |

#### 常用设置键

- `official_providers_seeded` - 官方 Provider 是否已初始化
- `common_config_claude` - Claude 通用配置 JSON
- `common_config_codex` - Codex 通用配置
- `common_config_opencode` - OpenCode 通用配置 JSON
- `optimizer_config` - 优化器配置
- `log_config` - 日志配置

### model_pricing

存储模型定价信息。

| 列名 | 类型 | 说明 |
|------|------|------|
| model_id | TEXT | 模型 ID |
| display_name | TEXT | 显示名称 |
| input_cost_per_million | TEXT | 每百万输入 token 成本 |
| output_cost_per_million | TEXT | 每百万输出 token 成本 |
| cache_read_cost_per_million | TEXT | 每百万缓存读取 token 成本 |
| cache_creation_cost_per_million | TEXT | 每百万缓存创建 token 成本 |

### provider_endpoints

存储 Provider 端点。

| 列名 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| provider_id | TEXT | Provider ID |
| app_type | TEXT | 平台类型 |
| url | TEXT | 端点 URL |
| added_at | INTEGER | 添加时间戳 |

### provider_health

存储 Provider 健康状态。

| 列名 | 类型 | 说明 |
|------|------|------|
| provider_id | TEXT | Provider ID |
| app_type | TEXT | 平台类型 |
| is_healthy | INTEGER | 是否健康 |
| consecutive_failures | INTEGER | 连续失败次数 |
| last_success_at | TEXT | 最后成功时间 |
| last_failure_at | TEXT | 最后失败时间 |
| last_error | TEXT | 最后错误 |
| updated_at | TEXT | 更新时间 |

### proxy_config

存储代理配置。

| 列名 | 类型 | 说明 |
|------|------|------|
| app_type | TEXT | 平台类型 |
| proxy_enabled | INTEGER | 是否启用代理 |
| listen_address | TEXT | 监听地址 |
| listen_port | INTEGER | 监听端口 |
| enable_logging | INTEGER | 是否启用日志 |
| enabled | INTEGER | 是否启用 |
| auto_failover_enabled | INTEGER | 是否启用自动故障转移 |
| max_retries | INTEGER | 最大重试次数 |
| streaming_first_byte_timeout | INTEGER | 流式首字节超时 |
| streaming_idle_timeout | INTEGER | 流式空闲超时 |
| non_streaming_timeout | INTEGER | 非流式超时 |
| circuit_failure_threshold | INTEGER | 熔断器失败阈值 |
| circuit_success_threshold | INTEGER | 熔断器成功阈值 |
| circuit_timeout_seconds | INTEGER | 熔断器超时秒数 |
| circuit_error_rate_threshold | REAL | 熔断器错误率阈值 |
| circuit_min_requests | INTEGER | 熔断器最小请求数 |
| default_cost_multiplier | TEXT | 默认成本倍数 |
| pricing_model_source | TEXT | 定价模型来源 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |
| live_takeover_active | INTEGER | 是否激活实时接管 |

### proxy_request_logs

存储请求日志。

| 列名 | 类型 | 说明 |
|------|------|------|
| request_id | TEXT | 请求 ID |
| provider_id | TEXT | Provider ID |
| app_type | TEXT | 平台类型 |
| model | TEXT | 模型 |
| request_model | TEXT | 请求模型 |
| input_tokens | INTEGER | 输入 token 数 |
| output_tokens | INTEGER | 输出 token 数 |
| cache_read_tokens | INTEGER | 缓存读取 token 数 |
| cache_creation_tokens | INTEGER | 缓存创建 token 数 |
| input_cost_usd | TEXT | 输入成本（美元） |
| output_cost_usd | TEXT | 输出成本（美元） |
| cache_read_cost_usd | TEXT | 缓存读取成本（美元） |
| cache_creation_cost_usd | TEXT | 缓存创建成本（美元） |
| total_cost_usd | TEXT | 总成本（美元） |
| latency_ms | INTEGER | 延迟（毫秒） |
| first_token_ms | INTEGER | 首字节延迟（毫秒） |
| duration_ms | INTEGER | 持续时间（毫秒） |
| status_code | INTEGER | 状态码 |
| error_message | TEXT | 错误信息 |
| session_id | TEXT | 会话 ID |
| provider_type | TEXT | Provider 类型 |
| is_streaming | INTEGER | 是否流式 |
| cost_multiplier | TEXT | 成本倍数 |
| created_at | INTEGER | 创建时间戳 |
| data_source | TEXT | 数据来源 |

### usage_daily_rollups

存储每日用量统计。

| 列名 | 类型 | 说明 |
|------|------|------|
| date | TEXT | 日期 |
| app_type | TEXT | 平台类型 |
| provider_id | TEXT | Provider ID |
| model | TEXT | 模型 |
| request_count | INTEGER | 请求数 |
| success_count | INTEGER | 成功数 |
| input_tokens | INTEGER | 输入 token 数 |
| output_tokens | INTEGER | 输出 token 数 |
| cache_read_tokens | INTEGER | 缓存读取 token 数 |
| cache_creation_tokens | INTEGER | 缓存创建 token 数 |
| total_cost_usd | TEXT | 总成本（美元） |
| avg_latency_ms | INTEGER | 平均延迟（毫秒） |

### stream_check_logs

存储流式检查日志。

| 列名 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| provider_id | TEXT | Provider ID |
| provider_name | TEXT | Provider 名称 |
| app_type | TEXT | 平台类型 |
| status | TEXT | 状态 |
| success | INTEGER | 是否成功 |
| message | TEXT | 消息 |
| response_time_ms | INTEGER | 响应时间（毫秒） |
| http_status | INTEGER | HTTP 状态码 |
| model_used | TEXT | 使用的模型 |
| retry_count | INTEGER | 重试次数 |
| tested_at | INTEGER | 测试时间戳 |

### session_log_sync

存储会话日志同步状态。

| 列名 | 类型 | 说明 |
|------|------|------|
| file_path | TEXT | 文件路径 |
| last_modified | INTEGER | 最后修改时间 |
| last_line_offset | INTEGER | 最后行偏移 |
| last_synced_at | INTEGER | 最后同步时间 |

### skill_repos

存储技能仓库。

| 列名 | 类型 | 说明 |
|------|------|------|
| owner | TEXT | 所有者 |
| name | TEXT | 名称 |
| branch | TEXT | 分支 |
| enabled | BOOLEAN | 是否启用 |
