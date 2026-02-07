"""
探索PDF内容，查看所有页面的文本和表格
"""
import pdfplumber


def explore_pdf(pdf_path: str):
    """探索PDF的所有内容"""
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF路径: {pdf_path}")
        print(f"总页数: {len(pdf.pages)}\n")
        
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"{'='*80}")
            print(f"第 {page_num} 页")
            print(f"{'='*80}\n")
            
            # 提取文本
            text = page.extract_text() or ""
            text_lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            print(f"文本行数: {len(text_lines)}")
            print("前20行文本:")
            for i, line in enumerate(text_lines[:20], start=1):
                print(f"  {i}. {line}")
            
            if len(text_lines) > 20:
                print(f"  ... (还有 {len(text_lines) - 20} 行)")
            
            # 提取表格
            tables = page.extract_tables()
            print(f"\n该页表格数量: {len(tables)}")
            
            for table_idx, table in enumerate(tables):
                print(f"\n  表格 {table_idx + 1}:")
                print(f"  尺寸: {len(table)} 行 x {len(table[0]) if table else 0} 列")
                
                # 显示前5行
                print("  前5行内容:")
                for row_idx, row in enumerate(table[:5]):
                    cleaned_row = [cell.strip() if cell else "" for cell in row]
                    print(f"    行{row_idx}: {cleaned_row}")
                
                if len(table) > 5:
                    print(f"    ... (还有 {len(table) - 5} 行)")
                
                # 搜索百草枯
                paraquat_found = False
                for row_idx, row in enumerate(table):
                    row_text = " ".join([str(cell) for cell in row if cell])
                    if "百草枯" in row_text or "paraquat" in row_text.lower():
                        print(f"\n  ⭐⭐⭐ 在行{row_idx}找到百草枯!")
                        cleaned_row = [cell.strip() if cell else "" for cell in row]
                        print(f"  内容: {cleaned_row}")
                        paraquat_found = True
                
                if paraquat_found:
                    print("\n  显示该表格的完整内容以便分析:")
                    for row_idx, row in enumerate(table):
                        cleaned_row = [cell.strip() if cell else "" for cell in row]
                        print(f"    行{row_idx}: {cleaned_row}")
            
            print("\n")


def main():
    pdf_path = r"C:\Users\Administrator\Desktop\检验报告自动核查系统\资料\GB2763-2021-ys-splited.pdf"
    explore_pdf(pdf_path)


if __name__ == "__main__":
    main()
