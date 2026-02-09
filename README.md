# InspeX - 食品检测报告智能验证系统

> 一个基于 AI 的食品检测报告自动化验证平台，提供国标合规性检查、检测项目核对、方法验证等全方位智能分析服务。

## 📋 项目简介

InspeX 是一个专业的食品安全检测报告验证系统，通过 OCR 技术提取检测报告信息，结合 RAGFlow 知识库和国标数据库，自动完成检测报告的合规性验证和风险识别。

### 核心功能

- 🔍 **智能 PDF 解析** - 基于 PaddleOCR 的高精度表格识别和数据提取
- 📊 **多维度验证体系**
  - 国标文件有效性验证（GB 标准状态检查）
  - 检验项目合规性核查（基于食品安全监督抽检实施细则）
  - 检测方法合规性验证
  - 标准指标合理性核查
  - 评价依据合理性验证
- 🤖 **RAGFlow 智能检索** - 基于向量数据库的细则文档智能匹配
- 📝 **样品信息管理** - 委托单和标签信息的上传与核对
- 📈 **可视化报告** - 清晰直观的验证结果展示和 PDF 预览

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Windows / Linux / macOS
- 约 2GB 磁盘空间

### 安装步骤

#### 1. 克隆项目

```bash
git clone <repository-url>
cd PDFInfExtraction
```

#### 2. 创建虚拟环境

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

**注意**: 首次安装 PaddleOCR 时会自动下载模型文件（约 100MB），请耐心等待。

#### 4. 配置环境变量

复制配置模板并填写必要的 API 密钥:

```bash
cp config.local.example.json config.local.json
```

编辑 `config.local.json`:

```json
{
    "RAGFLOW_API_URL": "你的 RAGFlow API 地址",
    "RAGFLOW_API_KEY": "你的 RAGFlow API 密钥",
    "RAGFLOW_KB_ID": "细则知识库 ID",
    "RAGFLOW_KB_ID_GB": "国标知识库 ID"
}
```

#### 5. 准备参考文件

将以下文件放入 `static/files/` 目录:
- `2025年食品安全监督抽检实施细则.pdf`
- `GB 2763-2021.pdf` (或其他需要参考的国标文件)

#### 6. 启动服务

**开发模式:**
```bash
python src/app.py
```

**生产模式 (使用 Gunicorn):**
```bash
gunicorn -c gunicorn_config.py src.app:app
```

启动后访问: `http://localhost:5002`

---

## 📁 项目结构

```
PDFInfExtraction/
├── src/                          # 源代码目录
│   ├── app.py                    # Flask 主应用
│   ├── field_extractor.py        # 字段提取器
│   ├── html_table_parser.py      # HTML 表格解析
│   ├── ragflow_client.py         # RAGFlow 客户端
│   ├── ragflow_verifier.py       # RAGFlow 验证逻辑
│   ├── pdf_reader.py             # PDF 读取器
│   ├── paddleocr_enhanced.py     # PaddleOCR 增强版
│   ├── table_merger.py           # 表格合并工具
│   ├── item_name_matcher.py      # 项目名称匹配
│   ├── package_image_processor.py # 标签图片处理
│   └── gb_verifier/              # 国标验证模块
│       ├── runner.py             # 验证执行器
│       ├── http_client.py        # HTTP 客户端
│       ├── html_extractor.py     # HTML 提取器
│       ├── screenshot.py         # 截图工具
│       └── download.py           # 文件下载
├── templates/                    # HTML 模板
│   ├── index.html                # 首页
│   └── result.html               # 结果页
├── static/                       # 静态资源
│   ├── style.css                 # 样式文件
│   ├── page_jump.js              # 页面跳转脚本
│   ├── files/                    # 参考文件目录
│   ├── uploads/                  # 上传文件目录
│   ├── screenshots/              # 截图目录
│   └── downloads/                # 下载文件目录
├── examples/                     # 示例代码
├── requirements.txt              # 依赖清单
├── requirements.production.txt   # 生产环境依赖
├── gunicorn_config.py            # Gunicorn 配置
├── config.local.json             # 本地配置文件
└── README.md                     # 本文档
```

---

## 🔧 核心模块说明

### 1. PDF 解析模块

- **PaddleOCR**: 高精度 OCR 识别引擎
- **PyMuPDF**: PDF 文档处理
- **表格解析**: 智能识别和提取表格数据

### 2. 验证模块

#### 国标验证 (`gb_verifier/`)
- 自动查询 GB 标准的发布日期、实施日期、状态
- 支持截图和文件下载
- 缓存机制提高性能

#### RAGFlow 验证 (`ragflow_verifier.py`)
- 基于向量检索的智能文档匹配
- 检验项目完整性检查
- 检测方法一致性验证
- 标准指标合理性分析

### 3. Web 界面

- **Flask**: 轻量级 Web 框架
- **响应式设计**: 支持多设备访问
- **实时预览**: 内嵌 PDF 查看器
- **分标签页展示**: 清晰的验证结果分类

---

## 📊 使用流程

1. **上传报告** - 上传 PDF 格式的检测报告
2. **自动解析** - 系统自动提取关键信息（样品名称、检测项目、标准值、实测值等）
3. **智能验证** - 多维度自动验证分析
4. **查看结果** - 查看详细的验证报告和风险提示
5. **补充信息** (可选) - 上传委托单、标签图片等附加信息

---

## 🔑 配置说明

### 核心配置项

| 配置项 | 说明 | 必填 |
|--------|------|------|
| `RAGFLOW_API_URL` | RAGFlow API 服务地址 | 是 |
| `RAGFLOW_API_KEY` | RAGFlow API 密钥 | 是 |
| `RAGFLOW_KB_ID` | 细则知识库 ID | 是 |
| `RAGFLOW_KB_ID_GB` | 国标知识库 ID | 是 |
| `FASTGPT_API_KEY` | FastGPT API 密钥 | 否 |
| `FASTGPT_API_BASE` | FastGPT API 地址 | 否 |

### Gunicorn 配置

编辑 `gunicorn_config.py` 调整服务器参数:

```python
bind = "0.0.0.0:5002"      # 监听地址和端口
workers = 4                 # 工作进程数
timeout = 300               # 请求超时时间
```

---

## 🛠️ 开发指南

### 添加新的验证规则

1. 在 `src/ragflow_verifier.py` 中添加验证逻辑
2. 更新 `templates/result.html` 中的展示模板
3. 添加对应的前端样式

### 调试模式

启用 Flask 调试模式:

```python
# src/app.py
app.run(debug=True, host='0.0.0.0', port=5002)
```

### 日志配置

日志文件位置:
- 应用日志: `logs/app.log`
- 国标验证日志: `gb_verify.log`

---

## 📦 部署指南

### 生产环境部署

1. **安装生产环境依赖**:
```bash
pip install -r requirements.production.txt
```

2. **使用 Gunicorn 启动**:
```bash
gunicorn -c gunicorn_config.py src.app:app
```

3. **配置反向代理** (Nginx 示例):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker 部署 (可选)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-c", "gunicorn_config.py", "src.app:app"]
```

---

## 🧪 测试

### 运行单元测试

```bash
python -m pytest tests/
```

### 示例测试文件

项目包含示例代码用于测试各个模块:
- `examples/paddleocr_enhanced_example.py` - OCR 功能测试

---

## 📚 API 文档

### 主要接口

#### 1. 上传报告
```http
POST /upload
Content-Type: multipart/form-data

files: PDF 文件
```

#### 2. 国标验证
```http
POST /api/check_gb_validity
Content-Type: application/json

{
  "gb_codes": ["GB 2763-2021"],
  "production_date": "2024-01-01",
  "enable_screenshot": true,
  "enable_download": true
}
```

#### 3. 查询标准细则
```http
POST /api/query_standards
Content-Type: application/json

{
  "food_name": "食品名称"
}
```

---

## ⚠️ 常见问题

### Q: OCR 识别准确率不高？
**A**: 确保 PDF 清晰度足够，避免扫描件模糊。可以调整 `paddleocr_enhanced.py` 中的参数优化识别。

### Q: RAGFlow 连接失败？
**A**: 检查 `config.local.json` 中的 API 地址和密钥是否正确，确保网络连接正常。

### Q: 页面加载缓慢？
**A**: 首次加载会下载 PaddleOCR 模型，后续使用会自动缓存。可以预先下载模型文件。

### Q: 如何清理缓存？
**A**: 删除以下目录:
- `static/cache/` - 验证缓存
- `__pycache__/` - Python 编译缓存

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

- 项目维护者: [您的名字]
- Email: [your.email@example.com]
- 项目链接: [GitHub Repository URL]

---

## 🙏 致谢

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - 优秀的 OCR 引擎
- [RAGFlow](https://github.com/infiniflow/ragflow) - 强大的检索增强生成框架
- [Flask](https://flask.palletsprojects.com/) - 简洁的 Web 框架
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF 处理工具

---

## 📈 更新日志

### v1.0.0 (2026-02-09)
- ✨ 初始版本发布
- ✅ 完成核心验证功能
- ✅ 支持多维度报告分析
- ✅ 集成 RAGFlow 智能检索
- ✅ 优化前端界面和用户体验

---

**如有问题或建议，欢迎提交 Issue！** 🚀
