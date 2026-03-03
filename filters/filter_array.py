"""
滤波器阵列模块
"""

import numpy as np

class FilterArray:
    """
    滤波器阵列类
    """
    
    def __init__(self, wavelength_range=(400, 700), num_wavelengths=301, num_filters=64):
        """
        初始化滤波器阵列
        
        Args:
            wavelength_range: 波长范围 (min, max) in nm
            num_wavelengths: 波长点数
            num_filters: 滤波器数量
        """
        self.wavelength_range = wavelength_range
        self.num_wavelengths = num_wavelengths
        self.num_filters = num_filters
        self.wavelengths = np.linspace(
            wavelength_range[0], wavelength_range[1], num_wavelengths
        )
        
        # 生成滤波器响应
        self.filters = self._generate_filters()
    
    def _generate_filters(self):
        """
        生成滤波器响应
        
        Returns:
            滤波器响应矩阵
        """
        filters = np.zeros((self.num_filters, self.num_wavelengths))
        
        # 生成不同中心波长的高斯滤波器
        center_wavelengths = np.linspace(
            self.wavelength_range[0],
            self.wavelength_range[1],
            self.num_filters
        )
        
        # 滤波器带宽
        bandwidth = (self.wavelength_range[1] - self.wavelength_range[0]) / self.num_filters * 1.5
        
        for i, center in enumerate(center_wavelengths):
            # 高斯滤波器
            filters[i] = np.exp(-((self.wavelengths - center) / bandwidth) ** 2)
        
        return filters
    
    def get_response_matrix(self):
        """
        获取响应矩阵
        
        Returns:
            响应矩阵
        """
        return self.filters
    
    def get_filter_response(self, filter_index):
        """
        获取单个滤波器的响应
        
        Args:
            filter_index: 滤波器索引
        
        Returns:
            滤波器响应
        """
        return self.filters[filter_index]
    
    def visualize_filters(self, num_filters=5):
        """
        可视化滤波器响应
        
        Args:
            num_filters: 要可视化的滤波器数量
        """
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        for i in range(min(num_filters, self.num_filters)):
            plt.plot(self.wavelengths, self.filters[i], label=f'Filter {i+1}')
        plt.title('Filter Responses')
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Response')
        plt.legend()
        plt.show()