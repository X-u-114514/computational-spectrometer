"""
性能评估器
"""

import numpy as np
from .metrics import calculate_mae, calculate_rmse, calculate_correlation

class PerformanceEvaluator:
    """
    性能评估器类
    """
    
    def __init__(self, wavelengths):
        """
        初始化性能评估器
        
        Args:
            wavelengths: 波长数组
        """
        self.wavelengths = wavelengths
    
    def evaluate_single_reconstruction(self, original, reconstructed):
        """
        评估单个重建结果
        
        Args:
            original: 原始光谱
            reconstructed: 重建光谱
        
        Returns:
            dict: 评估指标
        """
        # 计算评估指标
        mae = calculate_mae(original, reconstructed)
        rmse = calculate_rmse(original, reconstructed)
        correlation = calculate_correlation(original, reconstructed)
        
        return {
            "mae": mae,
            "rmse": rmse,
            "correlation": correlation
        }
    
    def evaluate_multiple_reconstructions(self, original_spectra, reconstructed_spectra):
        """
        评估多个重建结果
        
        Args:
            original_spectra: 原始光谱列表
            reconstructed_spectra: 重建光谱列表
        
        Returns:
            dict: 平均评估指标
        """
        maes = []
        rmses = []
        correlations = []
        
        for original, reconstructed in zip(original_spectra, reconstructed_spectra):
            metrics = self.evaluate_single_reconstruction(original, reconstructed)
            maes.append(metrics["mae"])
            rmses.append(metrics["rmse"])
            correlations.append(metrics["correlation"])
        
        return {
            "mean_mae": np.mean(maes),
            "mean_rmse": np.mean(rmses),
            "mean_correlation": np.mean(correlations),
            "std_mae": np.std(maes),
            "std_rmse": np.std(rmses),
            "std_correlation": np.std(correlations)
        }