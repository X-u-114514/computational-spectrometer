"""
计算光谱仪实现
"""

import numpy as np
from .base import BaseSpectrometer
from ..filters import FilterArray

class ComputationalSpectrometer(BaseSpectrometer):
    """
    计算光谱仪类
    """
    
    def __init__(self, wavelength_range=(400, 700), num_wavelengths=301, num_channels=64):
        """
        初始化计算光谱仪
        
        Args:
            wavelength_range: 波长范围 (min, max) in nm
            num_wavelengths: 波长点数
            num_channels: 通道数
        """
        super().__init__(wavelength_range, num_wavelengths)
        self.num_channels = num_channels
        self.filter_array = FilterArray(
            wavelength_range=wavelength_range,
            num_wavelengths=num_wavelengths,
            num_filters=num_channels
        )
        self.response_matrix = self.filter_array.get_response_matrix()
    
    def modulate(self, spectrum):
        """
        调制光谱
        
        Args:
            spectrum: 输入光谱
        
        Returns:
            调制后的信号
        """
        # 计算每个通道的响应
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