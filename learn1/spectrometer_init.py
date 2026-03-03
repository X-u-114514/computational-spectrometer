"""
模块1：光谱仪初始化
"""
import sys
import os

# 设置Python路径
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

from computational_spectrometer.core import ComputationalSpectrometer

def init_spectrometer():
    """
    初始化计算光谱仪
    
    Returns:
        ComputationalSpectrometer: 计算光谱仪实例
    """
    print("=== 模块1：初始化计算光谱仪 ===")
    
    # 创建计算光谱仪实例
    spectrometer = ComputationalSpectrometer(
        wavelength_range=(400, 700),
        num_wavelengths=301,
        num_channels=64
    )
    
    print(f"波长范围: {spectrometer.wavelength_range}")
    print(f"波长点数: {spectrometer.num_wavelengths}")
    print(f"通道数: {spectrometer.num_channels}")
    print()
    
    return spectrometer

if __name__ == "__main__":
    # 独立运行此模块
    spectrometer = init_spectrometer()
    print("光谱仪初始化成功！")