"""
傅里叶变换光谱仪实现
"""

import numpy as np
from .base import BaseSpectrometer

class FourierTransformSpectrometer(BaseSpectrometer):
    """
    傅里叶变换光谱仪类
    """
    
    def __init__(self, wavelength_range=(400, 700), max_opd=1000.0, apodization="hann"):
        """
        初始化傅里叶变换光谱仪
        
        Args:
            wavelength_range: 波长范围 (min, max) in nm
            max_opd: 最大光程差 in nm
            apodization: 切趾函数类型
        """
        # 计算波长点数 - 基于Nyquist采样定理
        num_wavelengths = int(2 * max_opd / (wavelength_range[0] ** 2 / wavelength_range[1])) + 1
        super().__init__(wavelength_range, num_wavelengths)
        
        self.max_opd = max_opd
        self.apodization = apodization
        
        # 计算光程差采样点
        self.num_points = num_wavelengths
        self.opd = np.linspace(0, max_opd, self.num_points)
        
        # 生成切趾函数
        self.apodization_function = self._get_apodization_function()
    
    def _get_apodization_function(self):
        """
        获取切趾函数
        
        Returns:
            切趾函数数组
        """
        if self.apodization == "hann":
            return 0.5 * (1 - np.cos(2 * np.pi * np.arange(self.num_points) / (self.num_points - 1)))
        elif self.apodization == "hamming":
            return 0.54 - 0.46 * np.cos(2 * np.pi * np.arange(self.num_points) / (self.num_points - 1))
        elif self.apodization == "blackman":
            return 0.42 - 0.5 * np.cos(2 * np.pi * np.arange(self.num_points) / (self.num_points - 1)) + 0.08 * np.cos(4 * np.pi * np.arange(self.num_points) / (self.num_points - 1))
        else:
            return np.ones(self.num_points)
    
    def modulate(self, spectrum):
        """
        调制光谱（生成干涉图）
        
        Args:
            spectrum: 输入光谱
        
        Returns:
            干涉图
        """
        # 计算干涉图
        interferogram = np.zeros(self.num_points)
        
        for i, opd in enumerate(self.opd):
            # 对每个波长计算相位差
            phase = 2 * np.pi * opd / (self.wavelengths * 1e-9)  # 转换为弧度
            # 计算干涉信号
            interferogram[i] = np.sum(spectrum * (1 + np.cos(phase)))
        
        # 应用切趾函数
        interferogram *= self.apodization_function
        
        return interferogram
    
    def demodulate(self, signal, method="fft", **kwargs):
        """
        解调信号（从干涉图恢复光谱）
        
        Args:
            signal: 干涉图
            method: 解调方法
            **kwargs: 额外参数
        
        Returns:
            解调后的光谱
        """
        if method == "fft":
            # 使用FFT解调
            fft_result = np.fft.fft(signal)
            
            # 计算频率轴
            frequencies = np.fft.fftfreq(self.num_points, d=self.opd[1] - self.opd[0])
            
            # 将频率转换为波长
            wavelengths = 1 / frequencies * 2e-9  # 2是因为光程差往返
            
            # 只取正频率部分
            positive_freqs = frequencies > 0
            wavelengths = wavelengths[positive_freqs]
            spectrum = np.abs(fft_result[positive_freqs])
            
            # 对波长进行排序
            sorted_indices = np.argsort(wavelengths)
            wavelengths = wavelengths[sorted_indices]
            spectrum = spectrum[sorted_indices]
            
            # 插值到原始波长网格
            reconstructed = np.interp(self.wavelengths, wavelengths * 1e9, spectrum, left=0, right=0)
            
            # 归一化
            if np.max(reconstructed) > 0:
                reconstructed /= np.max(reconstructed)
            
            return reconstructed
        else:
            # 使用通用解调方法
            from ..demodulation import demodulate
            # 构建响应矩阵
            response_matrix = np.zeros((self.num_points, self.num_wavelengths))
            for i, opd in enumerate(self.opd):
                phase = 2 * np.pi * opd / (self.wavelengths * 1e-9)
                response_matrix[i] = 1 + np.cos(phase)
            response_matrix *= self.apodization_function[:, np.newaxis]
            
            return demodulate(signal, response_matrix, method=method, **kwargs)