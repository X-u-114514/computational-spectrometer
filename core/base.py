"""
基础光谱仪类
"""

import numpy as np
from abc import ABC, abstractmethod

class BaseSpectrometer(ABC):
    """
    基础光谱仪抽象类
    """
    
    def __init__(self, wavelength_range=(400, 700), num_wavelengths=301):
        """
        初始化光谱仪
        
        Args:
            wavelength_range: 波长范围 (min, max) in nm
            num_wavelengths: 波长点数
        """
        self.wavelength_range = wavelength_range
        self.num_wavelengths = num_wavelengths
        self.wavelengths = np.linspace(
            wavelength_range[0], wavelength_range[1], num_wavelengths
        )
    
    @abstractmethod
    def modulate(self, spectrum):
        """
        调制光谱
        
        Args:
            spectrum: 输入光谱
        
        Returns:
            调制后的信号
        """
        pass
    
    @abstractmethod
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
        pass
    
    def simulate_full_chain(self, spectrum, demod_method="least_squares", **kwargs):
        """
        模拟完整的光谱仪链路
        
        Args:
            spectrum: 输入光谱
            demod_method: 解调方法
            **kwargs: 额外参数
        
        Returns:
            dict: 包含原始光谱、调制信号和解调光谱的字典
        """
        signal = self.modulate(spectrum)
        reconstructed = self.demodulate(signal, method=demod_method, **kwargs)
        
        return {
            "original": spectrum,
            "signal": signal,
            "reconstructed": reconstructed
        }