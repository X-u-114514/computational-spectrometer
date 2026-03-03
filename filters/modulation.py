"""
调制矩阵模块
"""

import numpy as np

class ModulationMatrix:
    """
    调制矩阵类
    """
    
    def __init__(self, wavelength_range=(400, 700), num_wavelengths=301, num_channels=64):
        """
        初始化调制矩阵
        
        Args:
            wavelength_range: 波长范围 (min, max) in nm
            num_wavelengths: 波长点数
            num_channels: 通道数
        """
        self.wavelength_range = wavelength_range
        self.num_wavelengths = num_wavelengths
        self.num_channels = num_channels
        self.wavelengths = np.linspace(
            wavelength_range[0], wavelength_range[1], num_wavelengths
        )
        
        # 生成调制矩阵
        self.matrix = self._generate_matrix()
    
    def _generate_matrix(self):
        """
        生成调制矩阵
        
        Returns:
            调制矩阵
        """
        # 生成随机调制矩阵
        matrix = np.random.rand(self.num_channels, self.num_wavelengths)
        
        # 归一化
        matrix = matrix / np.max(matrix, axis=1, keepdims=True)
        
        return matrix
    
    def get_matrix(self):
        """
        获取调制矩阵
        
        Returns:
            调制矩阵
        """
        return self.matrix
    
    def set_matrix(self, matrix):
        """
        设置调制矩阵
        
        Args:
            matrix: 新的调制矩阵
        """
        if matrix.shape != (self.num_channels, self.num_wavelengths):
            raise ValueError(f"Matrix shape must be ({self.num_channels}, {self.num_wavelengths})")
        self.matrix = matrix