from functools import lru_cache

from paddleocr import PaddleOCR


@lru_cache(maxsize=1)
def get_ocr_engine() -> PaddleOCR:
    """Create and cache a global PaddleOCR engine instance.

    默认使用中文模型，并开启方向分类器。第一次调用时会自动下载模型，耗时可能稍长。"""
    return PaddleOCR(use_angle_cls=True, lang="ch")
