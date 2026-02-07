"""
在PDF中直接搜索百草枯相关内容
"""
import pdfplumber
import json
import re


def search_paraquat_in_pdf(pdf_path: str):
    """在PDF中搜索百草枯相关内容"""
    
    paraquat_pages = []
    paraquat_details = []
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF路径: {pdf_path}")
        print(f"总页数: {len(pdf.pages)}")
        print(f"正在搜索包含'百草枯'的页面...\n")
        
        # 遍历所有页面
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            
            # 搜索百草枯
            if "百草枯" in text or "paraquat" in text.lower():
                print(f"{'='*80}")
                print(f"在第 {page_num} 页找到百草枯相关内容")
                print(f"{'='*80}\n")
                
                paraquat_pages.append(page_num)
                
                # 显示相关文本行
                text_lines = text.split('\n')
                print("包含百草枯的文本行:")
                for line_idx, line in enumerate(text_lines):
                    if "百草枯" in line or "paraquat" in line.lower():
                        print(f"  行{line_idx}: {line.strip()}")
                print()
                
                # 检查是否有表格标题
                table_match = re.search(r'表\s*(\d+)', text)
                if table_match:
                    table_num = table_match.group(1)
                    print(f"该页包含表格标记: 表{table_num}\n")
                
                # 提取该页的所有表格
                tables = page.extract_tables()
                print(f"该页共有 {len(tables)} 个表格\n")
                
                for table_idx, table in enumerate(tables):
                    print(f"--- 表格 {table_idx + 1} ---")
                    print(f"尺寸: {len(table)} 行 x {len(table[0]) if table else 0} 列\n")
                    
                    if table and len(table) > 0:
                        # 显示表头
                        print(f"表头: {table[0]}\n")
                        
                        # 搜索包含百草枯的行
                        for row_idx, row in enumerate(table):
                            row_text = " ".join([str(cell) if cell else "" for cell in row])
                            if "百草枯" in row_text:
                                cleaned_row = [cell.strip() if cell else "" for cell in row]
                                print(f"⭐ 行{row_idx}包含百草枯:")
                                print(f"   {cleaned_row}")
                                
                                paraquat_details.append({
                                    "page": page_num,
                                    "table_index": table_idx + 1,
                                    "row_index": row_idx,
                                    "row_data": cleaned_row
                                })
                        
                        # 如果表格很大，显示前几行作为示例
                        if len(table) > 10:
                            print(f"\n表格较大({len(table)}行)，显示前5行和包含百草枯的行:")
                            for i in range(min(5, len(table))):
                                print(f"  行{i}: {[cell[:20] if cell else '' for cell in table[i]]}")
                        else:
                            # 显示完整表格
                            print("\n完整表格内容:")
                            for i, row in enumerate(table):
                                print(f"  行{i}: {[cell.strip() if cell else '' for cell in row]}")
                    
                    print()
                
                print(f"{'='*80}\n")
        
        # 汇总结果
        print(f"\n{'='*80}")
        print("搜索结果汇总")
        print(f"{'='*80}\n")
        print(f"包含百草枯的页面数: {len(paraquat_pages)}")
        print(f"包含百草枯的页面: {paraquat_pages}")
        print(f"百草枯相关表格行数: {len(paraquat_details)}\n")
        
        # 详细分析
        if paraquat_details:
            print(f"{'='*80}")
            print("百草枯详细信息")
            print(f"{'='*80}\n")
            
            # 按页面分组
            by_page = {}
            for detail in paraquat_details:
                page = detail['page']
                if page not in by_page:
                    by_page[page] = []
                by_page[page].append(detail)
            
            for page, details in sorted(by_page.items()):
                print(f"\n第 {page} 页的百草枯信息:")
                for idx, detail in enumerate(details, start=1):
                    print(f"\n  记录 {idx}:")
                    print(f"    表格: {detail['table_index']}, 行: {detail['row_index']}")
                    print(f"    数据: {detail['row_data']}")
                    
                    # 尝试解析残留限量
                    row = detail['row_data']
                    if len(row) >= 2:
                        print(f"    → 农药: {row[0]}")
                        if len(row) >= 2:
                            print(f"    → 食品: {row[1]}")
                        if len(row) >= 3:
                            print(f"    → 限量: {row[2]}")
                        # 显示所有非空列
                        for i, cell in enumerate(row):
                            if cell and i > 2:
                                print(f"    → 列{i}: {cell}")
        
        # 保存结果
        result = {
            "pdf_path": pdf_path,
            "total_pages": len(pdf.pages),
            "paraquat_pages": paraquat_pages,
            "paraquat_details": paraquat_details
        }
        
        output_path = r"c:\Users\Administrator\Desktop\检验报告自动核查系统\PDFInfExtraction\paraquat_search_result.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"\n\n完整搜索结果已保存到: {output_path}")
        
        return result


def main():
    # 首先尝试原始PDF
    pdf_path = r"C:\Users\Administrator\Desktop\检验报告自动核查系统\资料\GB2763-2021-ys.pdf"
    search_paraquat_in_pdf(pdf_path)


if __name__ == "__main__":
    main()
