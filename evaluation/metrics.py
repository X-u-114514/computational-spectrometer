"""
评估指标模块
"""

import numpy as np

def calculate_mae(original, reconstructed):
    """
    计算平均绝对误差
    
    Args:
        original: 原始光谱
        reconstructed: 重建光谱
    
    Returns:
        平均绝对误差
    """
    return np.mean(np.abs(original - reconstructed))

def calculate_rmse(original, reconstructed):
    """
    计算均方根误差
    
    Args:
        original: 原始光谱
        reconstructed: 重建光谱
    
    Returns:
        均方根误差
    """
    return np.sqrt(np.mean((original - reconstructed) ** 2))

def calculate_correlation(original, reconstructed):
    """
    计算相关系数
    
    Args:
        original: 原始光谱
        reconstructed: 重建光谱
    
    Returns:
        相关系数
    """
    if np.std(original) == 0 or np.std(reconstructed) == 0:
        return 0.0
    return np.corrcoef(original, reconstructed)[0, 1]