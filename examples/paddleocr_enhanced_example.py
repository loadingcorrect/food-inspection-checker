# -*- coding: utf-8 -*-
"""
PaddleOCR 增强版使用示例
演示如何使用 PaddleOCREnhanced 类提取表格
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent))

from src.paddleocr_enhanced import PaddleOCREnhanced


def example_basic_usage():
    """基础用法示例"""
    print("=== 示例1：基础用法 ===\n")
    
    # 1. 初始化
    extractor = PaddleOCREnhanced(lang='ch', use_gpu=False)
    
    # 2. 提取表格
    tables = extractor.extract_from_pdf(
        pdf_path="path/to/your/pdf.pdf",  # 修改为实际路径
        zoom=3.0,  # 3倍缩放
        output_dir="output"
    )
    
    # 3. 使用结果
    for i, table in enumerate(tables, 1):
        print(f"\n表格 {i}:")
        print(f"  类型: {table.get('type')}")
        print(f"  页码: {table.get('source_pages', [table.get('page')])}")
        print(f"  行数: {len(table.get('rows', []))}")


def example_step_by_step():
    """分步执行示例"""
    print("=== 示例2：分步执行 ===\n")
    
    extractor = PaddleOCREnhanced(lang='ch')
    
    # 步骤1：仅转图
    images = extractor.pdf_to_high_res_images(
        pdf_path="path/to/your/pdf.pdf",
        zoom=3.0,
        output_dir="temp_images"
    )
    print(f"\n生成了 {len(images)} 张高清图片")
    
    # 步骤2：OCR 识别
    tables_by_page = extractor.ocr_extract_tables(images)
    print(f"\n识别了 {len(tables_by_page)} 页的表格")
    
    # 步骤3：跨页合并
    final_tables = extractor.merge_cross_page_tables(tables_by_page)
    print(f"\n合并后共 {len(final_tables)} 个表格")
    
    # 步骤4：符号保留
    final_tables = extractor.apply_symbol_preservation(final_tables)
    print("\n符号保留处理完成")
    
    return final_tables


def example_custom_parameters():
    """自定义参数示例"""
    print("=== 示例3：自定义参数 ===\n")
    
    # 使用不同的参数
    extractor = PaddleOCREnhanced(lang='ch', use_gpu=False)
    
    # 调整相似度阈值
    extractor.merger.similarity_threshold = 0.7  # 更严格的跨页检测
    
    # 使用更高的 DPI
    tables = extractor.extract_from_pdf(
        pdf_path="path/to/your/pdf.pdf",
        zoom=4.0,  # 更高的缩放倍数
        output_dir="high_quality_output"
    )
    
    return tables


def example_integration_with_existing_code():
    """与现有代码集成示例"""
    print("=== 示例4：与现有代码集成 ===\n")
    
    # 假设您已有的处理流程
    def your_existing_process(pdf_path):
        """您现有的处理流程"""
        # 原有代码...
        pass
    
    # 集成方式1：完全替换
    def new_process_v1(pdf_path):
        extractor = PaddleOCREnhanced(lang='ch')
        return extractor.extract_from_pdf(pdf_path, zoom=3.0)
    
    # 集成方式2：仅替换 PDF 转图部分
    def new_process_v2(pdf_path):
        extractor = PaddleOCREnhanced(lang='ch')
        
        # 使用高分辨率转图
        images = extractor.pdf_to_high_res_images(pdf_path, zoom=3.0)
        
        # 使用您原有的 OCR 方法
        # tables = your_existing_ocr_method(images)
        
        # 添加跨页合并
        # final_tables = extractor.merge_cross_page_tables(tables)
        
        return images  # 或 final_tables


def example_real_world_usage():
    """真实使用场景示例"""
    print("=== 示例5：真实场景 ===\n")
    
    # 配置
    PDF_PATH = r"C:\Users\Administrator\Desktop\extractionSystem\File\GB2763-2021-ys-splited.pdf"
    OUTPUT_DIR = r"C:\Users\Administrator\Desktop\extractionSystem\PDFInfExtraction\output"
    
    try:
        # 初始化
        print("正在初始化 PaddleOCR...")
        extractor = PaddleOCREnhanced(lang='ch', use_gpu=False)
        
        # 提取表格
        print(f"\n正在处理: {PDF_PATH}")
        tables = extractor.extract_from_pdf(
            pdf_path=PDF_PATH,
            zoom=3.0,
            output_dir=OUTPUT_DIR
        )
        
        # 保存结果
        import json
        result_file = Path(OUTPUT_DIR) / "extraction_result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(tables, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n结果已保存到: {result_file}")
        
        # 检查关键数据
        print("\n=== 关键数据检查 ===")
        for table in tables:
            html = table.get('html', '')
            if '百草枯' in html:
                print("✓ 找到'百草枯'")
            if '*' in html:
                print("✓ 找到星号符号")
            if '菜籽油' in html:
                print("✓ 找到'菜籽油'（跨页数据）")
        
        return tables
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 运行示例
    print("PaddleOCR Enhanced - 使用示例\n")
    
    # 选择要运行的示例
    # example_basic_usage()
    # example_step_by_step()
    # example_custom_parameters()
    # example_integration_with_existing_code()
    
    # 运行真实场景示例
    example_real_world_usage()
