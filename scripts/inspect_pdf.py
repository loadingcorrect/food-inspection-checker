"""
检查PDF的基本信息和内容
"""
import pdfplumber


def inspect_pdf(pdf_path: str):
    """检查PDF的基本信息"""
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"PDF路径: {pdf_path}")
        print(f"总页数: {len(pdf.pages)}\n")
        
        # 检查前几页的内容
        pages_to_check = min(5, len(pdf.pages))
        
        for page_num in range(pages_to_check):
            page = pdf.pages[page_num]
            print(f"{'='*80}")
            print(f"第 {page_num + 1} 页")
            print(f"{'='*80}\n")
            
            # 提取文本
            text = page.extract_text() or ""
            text_lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            print(f"文本行数: {len(text_lines)}")
            if text_lines:
                print("\n前10行文本:")
                for i, line in enumerate(text_lines[:10], start=1):
                    print(f"  {i}. {line}")
            else:
                print("无法提取文本（可能是扫描件）")
            
            # 提取表格
            tables = page.extract_tables()
            print(f"\n表格数量: {len(tables)}")
            
            if tables:
                print("\n第一个表格的前3行:")
                table = tables[0]
                for i in range(min(3, len(table))):
                    print(f"  {table[i]}")
            
            print("\n")
        
        # 搜索包含"表19"或"表 19"的页面
        print(f"{'='*80}")
        print("搜索包含'表19'或'表 19'的页面")
        print(f"{'='*80}\n")
        
        found_pages = []
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if "表19" in text or "表 19" in text or "表1 9" in text:
                found_pages.append(page_num)
                print(f"在第 {page_num} 页找到表格标记")
        
        if found_pages:
            print(f"\n共找到 {len(found_pages)} 个页面包含'表19'标记")
            print(f"页面: {found_pages}")
        else:
            print("\n未找到包含'表19'的页面")
        
        # 搜索"油料"和"油脂"相关页面
        print(f"\n{'='*80}")
        print("搜索包含'油料'或'油脂'的页面")
        print(f"{'='*80}\n")
        
        oil_pages = []
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if "油料" in text or "油脂" in text:
                oil_pages.append(page_num)
        
        if oil_pages:
            print(f"共找到 {len(oil_pages)} 个页面包含'油料'或'油脂'")
            print(f"前20个页面: {oil_pages[:20]}")
            
            # 显示第一个包含油料的页面的部分内容
            if oil_pages:
                first_page = pdf.pages[oil_pages[0] - 1]
                text = first_page.extract_text() or ""
                text_lines = [line.strip() for line in text.split('\n') if line.strip()]
                print(f"\n第 {oil_pages[0]} 页的前20行文本:")
                for i, line in enumerate(text_lines[:20], start=1):
                    print(f"  {i}. {line}")
        else:
            print("未找到包含'油料'或'油脂'的页面")


def main():
    pdf_path = r"C:\Users\Administrator\Desktop\检验报告自动核查系统\资料\GB2763-2021-ys.pdf"
    inspect_pdf(pdf_path)


if __name__ == "__main__":
    main()
