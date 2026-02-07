"""
FastGPT 客户端模块

用于查询食品检验标准和安全范围
"""
from __future__ import annotations

import os
import re
import requests
from typing import Any, Optional
from pathlib import Path


class FastGPTClient:
    """FastGPT 知识库客户端"""
    
    def __init__(self, api_key: str, api_base: str, knowledge_id: str):
        self.api_key = api_key
        self.api_base = api_base
        self.knowledge_id = knowledge_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def search(self, query: str, limit: int = 10, similarity: float = 0.1) -> dict[str, Any]:
        """
        搜索知识库
        
        参数:
            query: 查询文本
            limit: 返回结果数量
            similarity: 最低相似度阈值
        
        返回:
            搜索结果字典
        """
        search_url = f"{self.api_base}/core/dataset/searchTest"
        payload = {
            "datasetId": self.knowledge_id,
            "text": query,
            "limit": limit,
            "similarity": similarity
        }
        
        try:
            response = requests.post(
                search_url, 
                json=payload, 
                headers=self.headers, 
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"请求失败: {response.status_code}",
                    "message": response.text[:200]
                }
        except requests.exceptions.Timeout:
            return {"error": "请求超时"}
        except requests.exceptions.ConnectionError:
            return {"error": "连接错误"}
        except Exception as e:
            return {"error": f"异常: {str(e)}"}
    
    def get_best_result(self, query: str) -> Optional[dict[str, Any]]:
        """
        获取相似度最高的一条结果
        
        参数:
            query: 查询文本
        
        返回:
            最佳匹配结果，包含 content, page_number, similarity, source_name
        """
        result = self.search(query, limit=10)
        
        if "error" in result:
            return None
        
        if not isinstance(result, dict) or 'data' not in result:
            return None
        
        data = result['data']
        
        # 获取结果列表
        results_list = []
        if isinstance(data, list):
            results_list = data
        elif isinstance(data, dict) and 'list' in data:
            results_list = data['list']
        
        if not results_list:
            return None
        
        # 找到相似度最高的结果
        max_score = -1
        best_result = None
        
        for item in results_list:
            if isinstance(item, dict) and 'score' in item:
                score_item = item['score']
                if isinstance(score_item, list) and len(score_item) > 0:
                    similarity = score_item[0].get('value', 0)
                    if similarity > max_score:
                        max_score = similarity
                        best_result = item
        
        if not best_result:
            return None
        
        # 提取页码信息
        page_number = self._extract_page_number(best_result.get('q', ''))
        
        # 提取内容
        content = (
            best_result.get('content') or 
            best_result.get('text') or 
            best_result.get('q', '')
        )
        
        return {
            "content": content,
            "page_number": page_number,
            "similarity": max_score,
            "source_name": best_result.get('sourceName', '未知'),
            "raw_data": best_result
        }
    
    def _extract_page_number(self, text: str) -> str:
        """从文本中提取页码"""
        if not text:
            return ""
        
        # 查找页码模式
        page_match = re.search(
            r'检验项目(\d+)序号|(\d+)\s*序号|页码(\d+)|(\d+)$', 
            text
        )
        
        if page_match:
            return next((group for group in page_match.groups() if group), "")
        
        return ""


def query_inspection_items(food_name: str, config_path: str = "config.local.json") -> dict[str, Any]:
    """
    查询食品应检验项目
    
    参数:
        food_name: 食品名称
        config_path: 配置文件路径
    
    返回:
        {
            "success": True/False,
            "food_name": "黄瓜",
            "inspection_items": "...",
            "page_number": "155",
            "similarity": 0.95,
            "source_file": "2025年食品安全监督抽检实施细则.pdf"
        }
    """
    try:
        # 加载配置
        from verifier2.config import load_mcp_url
        
        # 尝试从配置文件加载
        config_file = Path(config_path)
        if config_file.exists():
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                api_key = config.get('FASTGPT_API_KEY')
                api_base = config.get('FASTGPT_API_BASE', 'https://cloud.fastgpt.cn/api')
                knowledge_id = config.get('FASTGPT_KNOWLEDGE_ID')
        else:
            # 使用环境变量
            api_key = os.getenv('FASTGPT_API_KEY')
            api_base = os.getenv('FASTGPT_API_BASE', 'https://cloud.fastgpt.cn/api')
            knowledge_id = os.getenv('FASTGPT_KNOWLEDGE_ID')
        
        if not api_key or not knowledge_id:
            return {
                "success": False,
                "error": "FastGPT 配置未设置"
            }
        
        # 创建客户端
        client = FastGPTClient(api_key, api_base, knowledge_id)
        
        # 构建查询
        query = f"{food_name} 检测项目"
        
        # 执行查询
        result = client.get_best_result(query)
        
        if not result:
            return {
                "success": False,
                "error": "未找到相关检验项目"
            }
        
        # 结果列表，用于前端结构化展示
        display_items = []
        
        # 处理 FastGPT 结果
        fastgpt_content = result['content']
        source_name = result.get('source_name', '')
        
        # 确定 PDF 文件 URL
        pdf_url = ""
        if "细则" in source_name:
            pdf_url = "/static/files/2025年食品安全监督抽检实施细则.pdf"
        elif "GB" in source_name or "2763" in source_name:
            pdf_url = "/static/files/GB 2763.1-2022 农残.pdf"
        
        display_items.append({
            "source": source_name or "检索结果",
            "title": "相关条目",
            "content": fastgpt_content,
            "page": result.get('page_number', ''),
            "file_url": pdf_url, 
            "similarity": result.get('similarity', 0)
        })

        return {
            "success": True,
            "food_name": food_name,
            "results": display_items
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": f"查询失败: {str(e)}"
        }
