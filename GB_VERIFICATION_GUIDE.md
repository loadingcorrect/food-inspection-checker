# 国标验证功能集成使用指南

## 功能概述

食品报告检测网页系统现已集成国标验证功能。当系统扫描PDF检验报告并提取国标编号后，会自动通过 Tavily MCP 从食品伙伴网检索国标信息，验证国标是否现行有效。

## 配置步骤

### 1. 配置 Tavily API Key

系统已为您创建了配置文件 `config.local.json`，其中包含您的 Tavily API Key：

```json
{
  "TAVILY_MCP_URL": "https://mcp.tavily.com/mcp/?tavilyApiKey=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"
}
```

> **注意**: 此文件已添加到 `.gitignore`，不会被提交到版本控制。

### 2. 安装依赖

```bash
cd C:\Users\Administrator\Desktop\extractionSystem\PDFInfExtraction
pip install -r requirements.txt
```

### 3. 启动应用

```bash
python src/app.py
```

应用将在 `http://localhost:5000` 启动。

## 使用方法

### 上传PDF并自动验证

1. 打开浏览器访问 `http://localhost:5000`
2. 上传包含国标信息的PDF检验报告
3. 系统会自动：
   - 提取食品名称、生产日期、国标编号
   - 调用验证服务检查国标有效性
   - 在结果页面显示验证状态

### 查看验证结果

在结果页面，您会看到：

- **国标有效性验证** 区域，显示每个国标的：
  - ✓ **现行有效** - 绿色徽章，表示国标当前有效
  - ✗ **已废止** - 红色徽章，表示国标已废止
  - **发布日期、实施日期、废止日期**
  - **食品伙伴网详情链接**
  - **不通过原因**（如果验证失败）

### 使用 API 接口

您也可以直接调用 API 接口验证国标：

```bash
curl -X POST http://localhost:5000/api/check_gb_validity \
  -H "Content-Type: application/json" \
  -d '{
    "gb_codes": ["GB 2763-2021", "GB 5009.1-2016"],
    "production_date": "2025-10-25"
  }'
```

返回示例：

```json
{
  "results": [
    {
      "code": "GB 2763-2021",
      "status": "valid",
      "status_text": "现行有效",
      "passed": true,
      "publish_date": "2021-03-15",
      "implement_date": "2021-09-15",
      "abolish_date": null,
      "detail_url": "https://down.foodmate.net/standard/sort/3/50617.html",
      "reasons": []
    }
  ]
}
```

## 验证逻辑

系统按以下顺序验证国标：

1. **标准状态检查**: 标准状态必须为"现行有效"
2. **实施日期检查**: 生产日期必须 >= 标准实施日期
3. **数据完整性检查**: 检查是否缺少关键信息

## 故障排查

### 验证功能不工作

- 检查 `config.local.json` 是否存在且包含正确的 API Key
- 检查网络连接是否正常
- 查看控制台是否有错误信息

### API Key 无效

如果 API Key 失效，请：

1. 获取新的 Tavily API Key
2. 更新 `config.local.json` 文件
3. 重启应用

### 验证结果显示"验证服务未配置"

这表示系统无法加载 MCP URL，请检查：

- `config.local.json` 文件是否存在
- 文件格式是否正确（有效的 JSON）
- `TAVILY_MCP_URL` 字段是否存在

## 技术架构

### 后端模块

- `src/verifier2/` - 国标验证核心模块（从同事的项目复制）
- `src/gb_verifier.py` - 验证功能包装模块
- `src/app.py` - Flask 应用，集成验证逻辑

### 前端

- `templates/result.html` - 结果页面模板，显示验证状态
- `static/style.css` - 样式文件，包含验证结果样式

### 数据流

```
PDF上传 → OCR提取 → 提取国标编号 → 调用验证服务 → 显示结果
                                    ↓
                            Tavily MCP → 食品伙伴网
```

## 数据来源

国标信息来自 [食品伙伴网标准下载中心](https://down.foodmate.net/standard/)。

## 注意事项

- 验证功能依赖外部 API，需要网络连接
- 验证过程可能需要几秒钟，请耐心等待
- 验证结果仅供参考，请以官方发布为准
- API 可能有调用限制，请合理使用
