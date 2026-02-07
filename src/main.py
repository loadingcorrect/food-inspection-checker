from __future__ import annotations

import argparse
import json
from pathlib import Path

from field_extractor import (
    extract_food_name,
    extract_gb_standards,
    extract_gb_standards_with_title,
    extract_inspection_items,
    extract_production_date,
)
from ocr_engine import get_ocr_engine
from pdf_reader import parse_pdf


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "读取食品抽检报告 PDF，自动提取样品名称/食品名称、生产日期和相关 GB 国家标准号。"
        )
    )
    parser.add_argument("pdf_path", help="待解析的 PDF 文件路径")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).expanduser().resolve()
    if not pdf_path.is_file():
        raise SystemExit(f"文件不存在: {pdf_path}")

    ocr_engine = get_ocr_engine()
    report = parse_pdf(str(pdf_path), ocr_engine=ocr_engine)

    food_name = extract_food_name(report)
    production_date = extract_production_date(report)
    gb_codes = extract_gb_standards(report)
    gb_detail = extract_gb_standards_with_title(report)

    summary = {
        "type": "summary",
        "file_path": str(pdf_path),
        "food_name": food_name,
        "production_date": production_date,
        "gb_codes": gb_codes,
        "gb_standards": gb_detail,
    }

    print(json.dumps(summary, ensure_ascii=False))

    items = extract_inspection_items(report)
    for item in items:
        print(json.dumps(item, ensure_ascii=False))


if __name__ == "__main__":
    main()
