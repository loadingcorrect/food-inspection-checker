"""
食品包装图片处理模块

处理食品包装图片，提取产品信息
"""
from __future__ import annotations

import re
from typing import Any, Optional


def extract_product_type(ocr_text: str) -> Optional[str]:
    """
    从OCR文本中提取产品类型
    
    常见模式：
    - 产品类型：纯牛奶
    - 产品类型: 灭菌乳
    - 类型：酸奶
    - 产品类别 灭菌乳
    """
    # 尝试多种模式
    patterns = [
        r'产品类型[：:\s]*([^\n\r]+)',
        r'类型[：:\s]*([^\n\r]+)',
        r'品类[：:\s]*([^\n\r]+)',
        r'产品类别[：:\s]*([^\n\r]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, ocr_text)
        if match:
            product_type = match.group(1).strip()
            # Remove leading colon if regex matched space but colon was part of value
            product_type = product_type.lstrip(':：')
            product_type = product_type.strip()
            # 清理可能的杂质
            product_type = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]+$', '', product_type)
            if product_type:
                return product_type
    
    return None


def extract_standard_code(ocr_text: str) -> Optional[str]:
    """
    从OCR文本中提取产品标准号
    
    常见模式：
    - 产品标准号：GB 25190
    - 产品标准号: GB/T 19645
    - 执行标准：GB 25190
    - 产品标准代号 GB 25190
    """
    # 尝试多种模式，包含宽松的冒号匹配
    patterns = [
        r'产品标准[号代]*[：:\s]*([a-zA-Z]{1,4}[/\sT]*\s*\d+(?:-\d+)?)',
        r'执行标准[：:\s]*([a-zA-Z]{1,4}[/\sT]*\s*\d+(?:-\d+)?)',
        r'标准[号代][：:\s]*([a-zA-Z]{1,4}[/\sT]*\s*\d+(?:-\d+)?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, ocr_text, re.IGNORECASE)
        if match:
            standard_code = match.group(1).strip()
            # 标准化格式（去除多余空格）
            standard_code = re.sub(r'\s+', ' ', standard_code)
            return standard_code
    
    # 如果没有找到带标签的，尝试直接查找GB标准号
    # 放宽匹配：GB开头，后跟数字，可能包含T或/
    match = re.search(r'\b(GB[/\sT]*\s*\d+(?:-\d+)?)\b', ocr_text, re.IGNORECASE)
    if match:
        standard_code = match.group(1).strip()
        standard_code = re.sub(r'\s+', ' ', standard_code)
        return standard_code
    
    return None


def extract_production_date(ocr_text: str) -> Optional[str]:
    """
    从OCR文本中提取生产日期
    
    常见模式：
    - 生产日期：2024-01-15
    - 生产日期: 20240115
    """
    patterns = [
        r'生产日期[：:]\s*(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})',
        r'生产日期[：:]\s*(\d{8})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, ocr_text)
        if match:
            date_str = match.group(1)
            # 标准化日期格式
            date_str = re.sub(r'[年月]', '-', date_str)
            date_str = re.sub(r'日', '', date_str)
            return date_str
    
    return None


def extract_shelf_life(ocr_text: str) -> Optional[str]:
    """
    从OCR文本中提取保质期
    
    常见模式：
    - 保质期：6个月
    - 保质期: 常温密封保存6个月
    """
    patterns = [
        r'保质期[：:]\s*([^\n\r]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, ocr_text)
        if match:
            shelf_life = match.group(1).strip()
            # 提取主要信息（去除多余描述）
            # 如果包含"个月"或"天"，提取数字和单位
            simple_match = re.search(r'(\d+\s*[个]?[月天年])', shelf_life)
            if simple_match:
                return simple_match.group(1)
            return shelf_life
    
    return None


def process_package_image(image_path: str, ocr_engine) -> dict[str, Any]:
    """
    处理食品包装图片，提取产品信息
    
    参数:
        image_path: 图片文件路径
        ocr_engine: OCR引擎实例
    
    返回:
        包含产品信息的字典
        {
            "product_type": "纯牛奶",
            "standard_code": "GB 25190",
            "production_date": "2024-01-15",
            "shelf_life": "6个月",
            "raw_text": "原始OCR文本"
        }
    """
    # 使用OCR识别图片
    result = ocr_engine.ocr(image_path, cls=True)
    
    # 提取所有文本
    ocr_text = ""
    if result and len(result) > 0:
        for line in result[0]:
            if line and len(line) >= 2:
                text = line[1][0] if isinstance(line[1], tuple) else line[1]
                ocr_text += text + "\n"
    
    # 提取各个字段
    product_info = {
        "product_type": extract_product_type(ocr_text),
        "standard_code": extract_standard_code(ocr_text),
        "production_date": extract_production_date(ocr_text),
        "shelf_life": extract_shelf_life(ocr_text),
        "raw_text": ocr_text.strip()
    }
    
    return product_info
