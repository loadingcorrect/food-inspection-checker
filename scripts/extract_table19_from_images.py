"""
从图像中提取表19的内容
"""
from paddleocr import PaddleOCR
from PIL import Image
import json


def extract_table19_content(image_paths: list):
    """使用OCR提取表19的内容"""
    
    print("正在初始化PaddleOCR...")
    ocr = PaddleOCR(lang="ch")
    print("初始化完成\n")
    
    all_results = []
    table_data = {
        "paraquat_found": False,
        "all_text_lines": [],
        "oil_related_entries": []
    }
    
    for img_path in image_paths:
        print(f"{'='*80}")
        print(f"正在识别: {img_path}")
        print(f"{'='*80}\n")
        
        result = ocr.ocr(img_path)
        
        print(f"识别到 {len(result[0])} 个文本区域\n")
        
        text_lines = []
        for idx, line in enumerate(result[0]):
            text = line[1][0]
            confidence = line[1][1]
            text_lines.append(text)
            print(f"{idx + 1}. {text} (置信度: {confidence:.3f})")
            
            # 检查是否包含百草枯
            if "百草枯" in text or "paraquat" in text.lower() or "百" in text and "草" in text and "枯" in text:
                print(f"   ⭐⭐⭐ 可能包含百草枯!")
                table_data["paraquat_found"] = True
            
            # 检查是否包含油料相关内容
            if any(keyword in text for keyword in ["油料", "油脂", "棉籽", "大豆", "葵花", "花生", "芝麻", "油菜", "亚麻"]):
                print(f"   📍 油料/油脂相关内容")
                table_data["oil_related_entries"].append({
                    "image": img_path,
                    "line_index": idx + 1,
                    "text": text,
                    "confidence": confidence
                })
        
        print()
        table_data["all_text_lines"].extend(text_lines)
        all_results.append({
            "image": img_path,
            "text_lines": text_lines
        })
    
    # 汇总分析
    print(f"\n{'='*80}")
    print("提取结果汇总")
    print(f"{'='*80}\n")
    
    # 检查完整文本中是否有百草枯
    full_text = "\n".join(table_data["all_text_lines"])
    if "百草枯" in full_text or "paraquat" in full_text.lower():
        table_data["paraquat_found"] = True
    
    print(f"是否找到百草枯: {'是' if table_data['paraquat_found'] else '否'}")
    print(f"油料/油脂相关条目数: {len(table_data['oil_related_entries'])}\n")
    
    if table_data["oil_related_entries"]:
        print(f"{'='*80}")
        print("油料和油脂相关内容")
        print(f"{'='*80}\n")
        
        for idx, entry in enumerate(table_data["oil_related_entries"], start=1):
            print(f"{idx}. {entry['text']}")
    
    # 尝试识别表格结构
    print(f"\n{'='*80}")
    print("表19内容分析")
    print(f"{'='*80}\n")
    
    print("从图像中可以看到表19包含以下部分:")
    print("\n【表19 - 农药残留限量】")
    print("列: 食品类别/名称 | 最大残留限量(mg/kg)")
    print("\n从识别的文本中提取的关键信息:\n")
    
    # 整理文本
    for line in table_data["all_text_lines"]:
        # 跳过一些无关的行
        if len(line.strip()) < 2:
            continue
        if "GB" in line and "2763" in line:
            continue
        if line.strip() in ["18", "19"]:  # 页码
            continue
        
        print(f"  {line}")
    
    # 保存结果
    output_path = r"c:\Users\Administrator\Desktop\检验报告自动核查系统\PDFInfExtraction\table19_ocr_result.json"
    output_data = {
        "results": all_results,
        "analysis": table_data
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n完整结果已保存到: {output_path}")
    
    return output_data


def main():
    image_paths = [
        r"c:\Users\Administrator\Desktop\检验报告自动核查系统\PDFInfExtraction\pdf_images\page_001.png",
        r"c:\Users\Administrator\Desktop\检验报告自动核查系统\PDFInfExtraction\pdf_images\page_002.png"
    ]
    
    print("从表19的图像中提取文本内容...\n")
    extract_table19_content(image_paths)


if __name__ == "__main__":
    main()
