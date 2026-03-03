"""
随机散斑光谱仪实现
"""

import numpy as np
from .base import BaseSpectrometer

class RandomSpeckleSpectrometer(BaseSpectrometer):
    """
    随机散斑光谱仪类
    """
    
    def __init__(self, wavelength_range=(400, 700), num_pixels=256, speckle_size=5.0, correlation_length=20.0):
        """
        初始化随机散斑光谱仪
        
        Args:
            wavelength_range: 波长范围 (min, max) in nm
            num_pixels: 像素数
            speckle_size: 散斑大小
            correlation_length: 相关长度
        """
        super().__init__(wavelength_range)
        
        self.num_pixels = num_pixels
        self.speckle_size = speckle_size
        self.correlation_length = correlation_length
        
        # 生成随机散斑响应矩阵
        self.response_matrix = self._generate_speckle_matrix()
    
    def _generate_speckle_matrix(self):
        """
        生成随机散斑响应矩阵
        
        Returns:
            随机散斑响应矩阵
        """
        # 生成基础随机矩阵
        base_matrix = np.random.randn(self.num_pixels, self.num_wavelengths)
        
        # 应用相关性（模拟散斑的空间相关性）
        for i in range(self.num_pixels):
            for j in range(self.num_wavelengths):
                # 计算距离
                distance = np.sqrt((i - self.num_pixels/2)**2 + (j - self.num_wavelengths/2)**2)
                # 应用高斯相关性
                correlation = np.exp(-distance**2 / (2 * self.correlation_length**2))
                base_matrix[i, j] *= correlation
        
        # 归一化
        base_matrix = np.abs(base_matrix)
        max_vals = np.max(base_matrix, axis=1, keepdims=True)
        max_vals[max_vals == 0] = 1  # 避免除零
        response_matrix = base_matrix / max_vals
        
        return response_matrix
    
    def modulate(self, spectrum):
        """
        调制光谱
        
        Args:
            spectrum: 输入光谱
        
        Returns:
            调制后的信号
        """
        # 计算每个像素的响应
        signal = np.dot(self.response_matrix, spectrum)
        return signal
    
    def demodulate(self, signal, method="least_squares", **kwargs):
        """
        解调信号
        
        Args:
            signal: 输入信号
            method: 解调方法
            **kwargs: 额外参数
        
        Returns:
            解调后的光谱
        """
        from ..demodulation import demodulate
        return demodulate(signal, self.response_matrix, method=method, **kwargs)