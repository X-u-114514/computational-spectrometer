"""
探测器模型模块
"""

from .ccd_simulator import CCDSimulator, SpotArray
from .noise import add_noise

__all__ = ["CCDSimulator", "SpotArray", "add_noise"]