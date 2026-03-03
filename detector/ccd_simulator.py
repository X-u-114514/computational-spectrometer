"""
CCD探测器模拟器
"""

import numpy as np

class SpotArray:
    """
    光斑阵列类
    """
    
    def __init__(self, num_spots, spot_size=3):
        """
        初始化光斑阵列
        
        Args:
            num_spots: 光斑数量
            spot_size: 光斑大小
        """
        self.num_spots = num_spots
        self.spot_size = spot_size
        self.spots = np.zeros((num_spots, 2))  # (x, y) 坐标
        
        # 均匀分布光斑
        grid_size = int(np.ceil(np.sqrt(num_spots)))
        idx = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if idx < num_spots:
                    self.spots[idx] = [i, j]
                    idx += 1
    
    def evaluate(self, image):
        """
        评估光斑阵列在图像上的响应
        
        Args:
            image: 输入图像
        
        Returns:
            光斑阵列的响应
        """
        height, width = image.shape
        responses = np.zeros(self.num_spots)
        
        for i, (x, y) in enumerate(self.spots):
            # 计算光斑区域
            x_min = max(0, int(x - self.spot_size/2))
            x_max = min(width, int(x + self.spot_size/2 + 1))
            y_min = max(0, int(y - self.spot_size/2))
            y_max = min(height, int(y + self.spot_size/2 + 1))
            
            # 计算光斑区域的平均值
            if x_max > x_min and y_max > y_min:
                responses[i] = np.mean(image[y_min:y_max, x_min:x_max])
        
        return responses

class CCDSimulator:
    """
    CCD探测器模拟器
    """
    
    def __init__(self, pixels=(64, 64), quantum_efficiency=0.8, dark_current=1e-9, read_noise=10):
        """
        初始化CCD模拟器
        
        Args:
            pixels: 像素尺寸 (height, width)
            quantum_efficiency: 量子效率
            dark_current: 暗电流 (A/pixel)
            read_noise: 读出噪声 (e-)
        """
        self.pixels = pixels
        self.quantum_efficiency = quantum_efficiency
        self.dark_current = dark_current
        self.read_noise = read_noise
    
    def simulate(self, signal, exposure_time=1.0):
        """
        模拟CCD探测器响应
        
        Args:
            signal: 输入信号
            exposure_time: 曝光时间 (s)
        
        Returns:
            模拟的探测器输出
        """
        # 将信号转换为光子数
        photons = signal * exposure_time * self.quantum_efficiency
        
        # 添加泊松噪声（光子噪声）
        photons = np.random.poisson(photons)
        
        # 添加暗电流噪声
        dark_noise = self.dark_current * exposure_time
        photons += np.random.poisson(dark_noise, size=self.pixels)
        
        # 添加读出噪声
        read_noise = np.random.normal(0, self.read_noise, size=self.pixels)
        photons = photons + read_noise
        
        # 确保非负
        photons = np.maximum(photons, 0)
        
        return photons
    
    def detect_spots(self, image, spot_array):
        """
        检测图像中的光斑
        
        Args:
            image: 输入图像
            spot_array: 光斑阵列
        
        Returns:
            光斑的响应
        """
        return spot_array.evaluate(image)