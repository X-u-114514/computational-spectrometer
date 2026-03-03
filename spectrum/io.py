"""
光谱IO模块
"""

import numpy as np

def load_spectrum(file_path):
    """
    加载光谱
    
    Args:
        file_path: 文件路径
    
    Returns:
        tuple: (波长, 光谱)
    """
    data = np.loadtxt(file_path)
    wavelengths = data[:, 0]
    spectrum = data[:, 1]
    return wavelengths, spectrum

def save_spectrum(file_path, wavelengths, spectrum):
    """
    保存光谱
    
    Args:
        file_path: 文件路径
        wavelengths: 波长数组
        spectrum: 光谱数组
    """
    data = np.column_stack((wavelengths, spectrum))
    np.savetxt(file_path, data, header="Wavelength (nm)\tIntensity")