"""
模块6：标定过程
"""
import sys
import os
import numpy as np

# 设置Python路径
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

from computational_spectrometer.demodulation import Calibrator

def perform_calibration(spectrometer):
    """
    执行标定过程
    
    Args:
        spectrometer: 光谱仪实例
    
    Returns:
        numpy.ndarray: 标定矩阵
    """
    print("=== 模块6：标定过程 ===")
    
    # 创建标定器
    calibrator = Calibrator(spectrometer, num_wavelengths=spectrometer.num_wavelengths, num_channels=spectrometer.num_channels)
    
    # 执行标定
    calibration_matrix = calibrator.calibrate(method="direct")
    print(f"标定矩阵形状: {calibration_matrix.shape}")
    
    # 保存标定矩阵
    np.save('calibration_matrix.npy', calibration_matrix)
    print("标定矩阵已保存为 learn1/calibration_matrix.npy")
    print()
    
    return calibration_matrix

if __name__ == "__main__":
    # 独立运行此模块
    from spectrometer_init import init_spectrometer
    spectrometer = init_spectrometer()
    calibration_matrix = perform_calibration(spectrometer)
    print("标定过程完成！")