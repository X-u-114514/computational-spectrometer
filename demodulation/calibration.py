"""
光谱仪标定模块
"""

import numpy as np
from .algorithms import LeastSquaresDemodulator

class Calibrator:
    """
    光谱仪标定器
    """
    
    def __init__(self, spectrometer, num_wavelengths=None, num_channels=None):
        """
        初始化标定器
        
        Args:
            spectrometer: 光谱仪实例
            num_wavelengths: 波长点数
            num_channels: 通道数
        """
        self.spectrometer = spectrometer
        self.num_wavelengths = num_wavelengths or spectrometer.num_wavelengths
        self.num_channels = num_channels or spectrometer.num_channels if hasattr(spectrometer, 'num_channels') else spectrometer.num_pixels
    
    def generate_calibration_data(self, num_samples=21):
        """
        生成标定数据
        
        Args:
            num_samples: 标定样本数
        
        Returns:
            tuple: (标定信号, 标定光谱)
        """
        print("生成标定数据...")
        
        # 生成等间隔的波长点
        calibration_wavelengths = np.linspace(
            self.spectrometer.wavelength_range[0],
            self.spectrometer.wavelength_range[1],
            num_samples
        )
        
        # 生成标定光谱（单波长峰）
        calibration_spectra = []
        calibration_signals = []
        
        for i, wavelength in enumerate(calibration_wavelengths):
            # 生成单波长光谱
            spectrum = np.zeros(self.num_wavelengths)
            # 找到最接近的波长索引
            idx = np.argmin(np.abs(self.spectrometer.wavelengths - wavelength))
            spectrum[idx] = 1.0
            
            # 生成信号
            signal = self.spectrometer.modulate(spectrum)
            
            calibration_spectra.append(spectrum)
            calibration_signals.append(signal)
            
            if (i + 1) % 5 == 0:
                print(f"  完成 {i+1}/{num_samples}")
        
        return np.array(calibration_signals), np.array(calibration_spectra)
    
    def calibrate(self, method="direct", num_samples=21):
        """
        执行标定
        
        Args:
            method: 标定方法
            num_samples: 标定样本数
        
        Returns:
            标定矩阵
        """
        # 生成标定数据
        calibration_signals, calibration_spectra = self.generate_calibration_data(num_samples)
        
        if method == "direct":
            # 直接使用标定数据的伪逆作为标定矩阵
            calibration_matrix = np.linalg.pinv(calibration_signals)
        elif method == "least_squares":
            # 使用最小二乘拟合
            demodulator = LeastSquaresDemodulator()
            # 构建响应矩阵
            response_matrix = np.zeros((self.num_channels, self.num_wavelengths))
            for i, spectrum in enumerate(calibration_spectra):
                response_matrix[:, i] = calibration_signals[i]
            # 计算伪逆
            calibration_matrix = np.linalg.pinv(response_matrix)
        else:
            raise ValueError(f"Unknown calibration method: {method}")
        
        return calibration_matrix