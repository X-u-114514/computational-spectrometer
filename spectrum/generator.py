"""
光谱生成模块
"""

import numpy as np

def generate_spectrum(wavelengths, peaks=None):
    """
    生成光谱
    
    Args:
        wavelengths: 波长数组
        peaks: 峰的列表，每个峰是一个字典，包含center, amplitude, width
    
    Returns:
        生成的光谱
    """
    if peaks is None:
        # 默认峰
        peaks = [
            {"center": 450, "amplitude": 1.0, "width": 20},
            {"center": 550, "amplitude": 0.8, "width": 30},
            {"center": 650, "amplitude": 0.6, "width": 25}
        ]
    
    spectrum = np.zeros_like(wavelengths)
    
    for peak in peaks:
        center = peak["center"]
        amplitude = peak["amplitude"]
        width = peak["width"]
        
        # 高斯峰
        spectrum += amplitude * np.exp(-((wavelengths - center) / width) ** 2)
    
    return spectrum

def generate_multi_peak_spectrum(wavelengths, num_peaks=3, min_amplitude=0.5, max_amplitude=1.0, min_width=10, max_width=30):
    """
    生成多峰光谱
    
    Args:
        wavelengths: 波长数组
        num_peaks: 峰的数量
        min_amplitude: 最小振幅
        max_amplitude: 最大振幅
        min_width: 最小宽度
        max_width: 最大宽度
    
    Returns:
        生成的光谱
    """
    # 随机生成峰的位置
    min_wavelength = np.min(wavelengths)
    max_wavelength = np.max(wavelengths)
    
    peaks = []
    for i in range(num_peaks):
        center = np.random.uniform(min_wavelength, max_wavelength)
        amplitude = np.random.uniform(min_amplitude, max_amplitude)
        width = np.random.uniform(min_width, max_width)
        
        peaks.append({
            "center": center,
            "amplitude": amplitude,
            "width": width
        })
    
    return generate_spectrum(wavelengths, peaks)