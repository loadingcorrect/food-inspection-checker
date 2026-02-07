"""
提取表20 - 百菌清在水果中的残留限量
测试跨页表格和一格多行的提取能力
"""
import fitz  # PyMuPDF
from PIL import Image
import os
import json


def convert_pdf_to_images(pdf_path: str, output_dir: str):
    """将PDF转换为高清图像"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"正在处理PDF: {pdf_path}\n")
    
    doc = fitz.open(pdf_path)
    print(f"PDF总页数: {len(doc)}\n")
    
    image_paths = []
    
    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            real_page_num = page_num + 1
            
            print(f"转换第 {real_page_num} 页...")
            
            # 高分辨率转换
            zoom = 3.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            mode = "RGBA" if pix.alpha else "RGB"
            image = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            if pix.alpha:
                image = image.convert("RGB")
            
            output_filename = f"table20_page_{real_page_num:03d}.png"
            output_path = os.path.join(output_dir, output_filename)
            image.save(output_path, "PNG", quality=95)
            
            image_paths.append(output_path)
            print(f"  保存: {output_filename} ({image.size[0]}x{image.size[1]} 像素)\n")
    
    finally:
        doc.close()
    
    print(f"{'='*80}")
    print("转换完成！")
    print(f"{'='*80}")
    print(f"共转换 {len(image_paths)} 页")
    print(f"图像保存在: {output_dir}\n")
    
    return image_paths


def main():
    pdf_path = r"C:\Users\Administrator\Desktop\检验报告自动核查系统\资料\GB2763-2021-ys-34-36.pdf"
    output_dir = r"c:\Users\Administrator\Desktop\检验报告自动核查系统\PDFInfExtraction\table20_images"
    
    if not os.path.exists(pdf_path):
        print(f"错误: PDF文件不存在: {pdf_path}")
        return
    
    print("="*80)
    print("表20提取测试 - 百菌清在水果中的残留限量")
    print("="*80)
    print()
    
    image_paths = convert_pdf_to_images(pdf_path, output_dir)
    
    print("\n提示:")
    print("1. 图像已保存，请查看识别表20的位置")
    print("2. 找到百菌清相关内容")
    print("3. 识别水果类别和残留限量值")
    
    # 保存路径信息
    result = {
        "pdf_path": pdf_path,
        "total_pages": len(image_paths),
        "image_paths": image_paths,
        "task": "提取表20中百菌清在水果中的最大残留限量"
    }
    
    output_json = os.path.join(output_dir, "extraction_info.json")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n信息已保存到: {output_json}")


if __name__ == "__main__":
    main()
