# 包装信息标签页完整代码

## 需要手动修改的文件

### 1. templates/index.html

**修改第49行**，将：
```html
<input type="file" name="pdfs" accept="application/pdf,image/jpeg,image/png,image/jpg" multiple id="fileInput" class="file-input-hidden" />
```

改为：
```html
<input type="file" name="pdfs" accept="application/pdf" multiple id="fileInput" class="file-input-hidden" />
```

**修改第59行**（大约），将：
```html
<p class="upload-hint">支持 PDF 和图片格式（JPG、PNG）</p>
```

改为：
```html
<p class="upload-hint">支持 PDF 格式</p>
```

---

### 2. templates/result.html

**在第348行（`// Tab switching` 注释之前）添加以下函数**：

```javascript
function renderPackageTab(result) {
  let html = '';
  
  // 显示上传区域
  html += `
    <div class="section-block">
      <h3 class="block-title">上传包装图片</h3>
      <div class="package-upload-section">
        <div class="upload-package-area">
          <input type="file" id="packageImageInput" accept="image/jpeg,image/png,image/jpg" style="display:none;" />
          <button class="btn-upload-package" onclick="document.getElementById('packageImageInput').click()">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            选择包装图片
          </button>
          <p class="upload-package-hint">支持 JPG、PNG 格式</p>
        </div>
        <div id="packageInfoDisplay" style="display:none;">
          <!-- 识别结果将显示在这里 -->
        </div>
      </div>
    </div>
  `;
  
  return html;
}

// 包装图片上传处理
document.addEventListener('DOMContentLoaded', function() {
  document.body.addEventListener('change', function(e) {
    if (e.target && e.target.id === 'packageImageInput') {
      const file = e.target.files[0];
      if (!file) return;
      
      const formData = new FormData();
      formData.append('image', file);
      
      // 显示加载状态
      const display = document.getElementById('packageInfoDisplay');
      if (display) {
        display.style.display = 'block';
        display.innerHTML = '<p style="text-align:center;padding:20px;">正在识别...</p>';
      }
      
      // 上传并识别
      fetch('/api/upload_package_image', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // 显示识别结果
          const info = data.data;
          let html = `
            <div class="section-block">
              <h3 class="block-title">产品信息</h3>
              <div class="info-grid-clean">
                <div class="info-cell">
                  <span class="label">产品类型</span>
                  <span class="value">${info.product_type || '<span class="empty">未识别</span>'}</span>
                </div>
                <div class="info-cell">
                  <span class="label">产品标准号</span>
                  <span class="value">${info.standard_code || '<span class="empty">未识别</span>'}</span>
                </div>
                ${info.production_date ? `
                  <div class="info-cell">
                    <span class="label">生产日期</span>
                    <span class="value">${info.production_date}</span>
                  </div>
                ` : ''}
                ${info.shelf_life ? `
                  <div class="info-cell">
                    <span class="label">保质期</span>
                    <span class="value">${info.shelf_life}</span>
                  </div>
                ` : ''}
              </div>
            </div>
          `;
          
          if (info.image_url) {
            html += `
              <div class="section-block">
                <h3 class="block-title">包装图片</h3>
                <div class="package-image-container">
                  <img src="${info.image_url}" alt="食品包装图片" class="package-image" />
                </div>
              </div>
            `;
          }
          
          display.innerHTML = html;
        } else {
          display.innerHTML = `<p style="color:red;padding:20px;">识别失败: ${data.error}</p>`;
        }
      })
      .catch(error => {
        display.innerHTML = `<p style="color:red;padding:20px;">上传失败: ${error.message}</p>`;
      });
    }
  });
});
```

---

### 3. static/style.css

**在文件末尾添加以下样式**（已经添加过了，无需重复）：

```css
/* Package Upload Section */
.package-upload-section {
  padding: 20px;
}

.upload-package-area {
  text-align: center;
  padding: 40px;
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  margin-bottom: 20px;
}

.btn-upload-package {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--color-brand);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-upload-package:hover {
  background: #0056b3;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.upload-package-hint {
  margin-top: 12px;
  color: var(--text-secondary);
  font-size: 13px;
}

/* Package Image Styles (已添加) */
.package-image-container {
  text-align: center;
  padding: 20px;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.package-image {
  max-width: 100%;
  max-height: 600px;
  border-radius: var(--radius-md);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
```

## 完成后的效果

1. 用户上传PDF报告后，查看结果
2. 点击"包装信息"标签页
3. 点击"选择包装图片"按钮上传图片
4. 系统自动识别并显示产品类型、标准号等信息
5. 显示上传的包装图片

## 测试步骤

1. 重启Flask应用
2. 上传一个PDF报告
3. 在结果页面点击"包装信息"标签页
4. 上传包装图片（如 `C:\Users\Administrator\Desktop\extractionSystem\File\纯牛奶.jpg`）
5. 查看识别结果
