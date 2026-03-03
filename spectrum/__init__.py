"""
光谱生成和处理模块
"""

from .generator import generate_spectrum, generate_multi_peak_spectrum
from .io import load_spectrum, save_spectrum

__all__ = [
    "generate_spectrum",
    "generate_multi_peak_spectrum",
    "load_spectrum",
    "save_spectrum"
]