# FastGPT 标准检索功能集成指南

## 已完成的工作

✅ 创建了 `src/fastgpt_client.py` 模块
✅ 添加了 FastGPT 配置到 `config.local.json`

## 需要手动完成的步骤

### 步骤1：在 app.py 中添加 API 接口

在 `src/app.py` 文件中：

**1.1 添加导入**（在文件开头，第11行后添加）：
```python
from fastgpt_client import query_inspection_items
```

**1.2 添加 API 接口**（在 `/api/upload_package_image` 接口后添加）：
```python
@app.route("/api/query_standards", methods=["POST"])
def query_standards():
    """
    查询食品检验标准
    
    输入:
    {
        "food_name": "黄瓜"
    }
    
    输出:
    {
        "success": true,
        "data": {
            "food_name": "黄瓜",
            "inspection_items": "...",
            "page_number": "155",
            "similarity": 0.95,
            "source_file": "2025年食品安全监督抽检实施细则.pdf"
        }
    }
    """
    try:
        data = request.get_json()
        food_name = data.get('food_name')
        
        if not food_name:
            return jsonify({
                "success": False,
                "error": "缺少食品名称"
            }), 400
        
        # 查询检验项目
        result = query_inspection_items(
            food_name=food_name,
            config_path=str(BASE_DIR / "config.local.json")
        )
        
        if result.get("success"):
            return jsonify({
                "success": True,
                "data": result
            })
        else:
            return jsonify(result), 500
    
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500
```

### 步骤2：修改 result.html 添加第4个标签页

**2.1 添加标签页按钮**（在第86行左右，"包装信息"按钮后添加）：
```html
<button class="tab-btn" data-tab="standards">标准检索</button>
```

**2.2 在 renderTabContent 函数中添加分支**（第140行左右）：
```javascript
} else if (tab === 'standards') {
  html = renderStandardsTab(result);
}
```

**2.3 添加 renderStandardsTab 函数**（在 renderPackageTab 函数后添加）：
```javascript
function renderStandardsTab(result) {
  let html = '';
  const s = result.summary;
  
  html += `
    <div class="section-block">
      <h3 class="block-title">查询检验标准</h3>
      <div class="standards-query-section">
        <div class="query-input-area">
          <div class="input-group">
            <label>食品名称</label>
            <input type="text" id="foodNameInput" value="${s.food_name || ''}" placeholder="请输入食品名称" />
          </div>
          <button class="btn-query-standards" onclick="queryStandards()">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            查询标准
          </button>
        </div>
        <div id="standardsResultDisplay" style="display:none;">
          <!-- 查询结果将显示在这里 -->
        </div>
      </div>
    </div>
  `;
  
  return html;
}

// 查询标准函数
function queryStandards() {
  const foodName = document.getElementById('foodNameInput').value.trim();
  
  if (!foodName) {
    alert('请输入食品名称');
    return;
  }
  
  const display = document.getElementById('standardsResultDisplay');
  if (display) {
    display.style.display = 'block';
    display.innerHTML = '<p style="text-align:center;padding:20px;">正在查询...</p>';
  }
  
  fetch('/api/query_standards', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      food_name: foodName
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      const info = data.data;
      let html = `
        <div class="section-block">
          <h3 class="block-title">检验项目</h3>
          <div class="standards-result">
            <div class="result-meta">
              <span class="meta-item"><strong>食品名称:</strong> ${info.food_name}</span>
              <span class="meta-item"><strong>相似度:</strong> ${(info.similarity * 100).toFixed(1)}%</span>
              ${info.page_number ? `<span class="meta-item"><strong>页码:</strong> ${info.page_number}</span>` : ''}
              <span class="meta-item"><strong>来源:</strong> ${info.source_file}</span>
            </div>
            <div class="result-content">
              <pre>${info.inspection_items}</pre>
            </div>
          </div>
        </div>
      `;
      
      display.innerHTML = html;
    } else {
      display.innerHTML = `<p style="color:red;padding:20px;">查询失败: ${data.error}</p>`;
    }
  })
  .catch(error => {
    display.innerHTML = `<p style="color:red;padding:20px;">查询失败: ${error.message}</p>`;
  });
}
```

### 步骤3：添加 CSS 样式

在 `static/style.css` 文件末尾添加：
```css
/* Standards Query Section */
.standards-query-section {
  padding: 20px;
}

.query-input-area {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  padding: 20px;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.input-group {
  flex: 1;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 14px;
}

.input-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
}

.input-group input:focus {
  outline: none;
  border-color: var(--color-brand);
}

.btn-query-standards {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--color-brand);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-query-standards:hover {
  background: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.standards-result {
  margin-top: 20px;
  padding: 20px;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.result-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-divider);
}

.meta-item {
  font-size: 13px;
  color: var(--text-secondary);
}

.meta-item strong {
  color: var(--text-primary);
}

.result-content {
  background: #f8f9fa;
  padding: 16px;
  border-radius: var(--radius-sm);
}

.result-content pre {
  margin: 0;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
}
```

## 测试步骤

1. 重启 Flask 应用
2. 上传一个PDF报告（如黄瓜检验报告）
3. 在结果页面点击"标准检索"标签页
4. 食品名称会自动填充（从报告中提取）
5. 点击"查询标准"按钮
6. 查看检验项目和标准信息

## 功能说明

- **输入**: 食品名称（自动从报告提取，也可手动修改）
- **处理**: 调用 FastGPT 知识库查询应检验项目
- **输出**: 
  - 检验项目详细内容
  - 页码信息
  - 相似度
  - 来源文件名

## 注意事项

- FastGPT 查询需要网络连接
- 查询结果基于知识库中的《2025年食品安全监督抽检实施细则.pdf》
- 相似度越高，结果越准确
