"""
将PDF页面转换为高质量图像以便查看和分析
"""
import fitz  # PyMuPDF
from PIL import Image
import os


def convert_pdf_pages_to_images(pdf_path: str, output_dir: str):
    """
    将PDF的所有页面转换为图像
    """
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"PDF路径: {pdf_path}")
    print(f"输出目录: {output_dir}\n")
    
    doc = fitz.open(pdf_path)
    print(f"PDF总页数: {len(doc)}\n")
    
    image_paths = []
    
    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            real_page_num = page_num + 1
            
            print(f"处理第 {real_page_num} 页...")
            
            # 使用高分辨率
            zoom = 3.0  # 3倍放大，约216 DPI
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # 转换为PIL Image
            mode = "RGBA" if pix.alpha else "RGB"
            image = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            if pix.alpha:
                image = image.convert("RGB")
            
            # 保存图像
            output_filename = f"page_{real_page_num:03d}.png"
            output_path = os.path.join(output_dir, output_filename)
            image.save(output_path, "PNG", quality=95)
            
            image_paths.append(output_path)
            
            print(f"  已保存: {output_filename}")
            print(f"  图像尺寸: {image.size[0]} x {image.size[1]} 像素\n")
    
    finally:
        doc.close()
    
    print(f"{'='*80}")
    print("转换完成!")
    print(f"{'='*80}")
    print(f"共转换 {len(image_paths)} 页")
    print(f"图像保存在: {output_dir}\n")
    
    return image_paths


def main():
    # 转换splited版本的PDF
    pdf_path = r"C:\Users\Administrator\Desktop\检验报告自动核查系统\资料\GB2763-2021-ys-splited.pdf"
    output_dir = r"c:\Users\Administrator\Desktop\检验报告自动核查系统\PDFInfExtraction\pdf_images"
    
    print("正在将PDF转换为高质量图像...")
    print("转换后可以直接查看图像来找到表19\n")
    
    image_paths = convert_pdf_pages_to_images(pdf_path, output_dir)
    
    print("\n提示:")
    print("1. 请打开输出目录查看图像")
    print("2. 找到包含表19和百草枯的页面")
    print("3. 记下页码后，可以对特定页面进行更精细的OCR识别")


if __name__ == "__main__":
    main()
