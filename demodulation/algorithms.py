"""
解调算法实现
"""

import numpy as np
from abc import ABC, abstractmethod

class BaseDemodulator(ABC):
    """
    基础解调器抽象类
    """
    
    @abstractmethod
    def demodulate(self, signal, response_matrix):
        """
        解调信号
        
        Args:
            signal: 输入信号
            response_matrix: 响应矩阵
        
        Returns:
            解调后的光谱
        """
        pass

class LeastSquaresDemodulator(BaseDemodulator):
    """
    最小二乘解调器
    """
    
    def demodulate(self, signal, response_matrix):
        """
        使用最小二乘法解调
        
        Args:
            signal: 输入信号
            response_matrix: 响应矩阵
        
        Returns:
            解调后的光谱
        """
        # 使用伪逆求解
        if response_matrix.shape[0] >= response_matrix.shape[1]:
            # 超定系统 - 使用最小二乘
            spectrum = np.linalg.lstsq(response_matrix, signal, rcond=None)[0]
        else:
            # 欠定系统 - 使用伪逆
            pseudo_inverse = np.linalg.pinv(response_matrix)
            spectrum = np.dot(pseudo_inverse, signal)
        
        # 确保光谱非负
        spectrum = np.maximum(spectrum, 0)
        return spectrum

class TikhonovDemodulator(BaseDemodulator):
    """
    Tikhonov正则化解调器
    """
    
    def __init__(self, regularization=0.01):
        """
        初始化Tikhonov解调器
        
        Args:
            regularization: 正则化参数
        """
        self.regularization = regularization
    
    def demodulate(self, signal, response_matrix):
        """
        使用Tikhonov正则化解调
        
        Args:
            signal: 输入信号
            response_matrix: 响应矩阵
        
        Returns:
            解调后的光谱
        """
        # 构建正则化矩阵（二阶差分）
        n = response_matrix.shape[1]
        D = np.zeros((n-2, n))
        for i in range(n-2):
            D[i, i] = 1
            D[i, i+1] = -2
            D[i, i+2] = 1
        
        # 构建增广矩阵
        A = np.vstack([response_matrix, self.regularization * D])
        b = np.hstack([signal, np.zeros(n-2)])
        
        # 求解
        spectrum = np.linalg.lstsq(A, b, rcond=None)[0]
        
        # 确保光谱非负
        spectrum = np.maximum(spectrum, 0)
        return spectrum

class LassoDemodulator(BaseDemodulator):
    """
    LASSO解调器
    """
    
    def __init__(self, alpha=0.001):
        """
        初始化LASSO解调器
        
        Args:
            alpha: 正则化参数
        """
        self.alpha = alpha
    
    def demodulate(self, signal, response_matrix):
        """
        使用LASSO解调
        
        Args:
            signal: 输入信号
            response_matrix: 响应矩阵
        
        Returns:
            解调后的光谱
        """
        try:
            from sklearn.linear_model import Lasso
            
            # 创建LASSO模型
            lasso = Lasso(alpha=self.alpha, positive=True, max_iter=10000)
            
            # 训练模型
            lasso.fit(response_matrix, signal)
            
            # 获取系数（光谱）
            spectrum = lasso.coef_
            
            return spectrum
        except ImportError:
            # 如果scikit-learn不可用，使用最小二乘
            print("scikit-learn not available, using least squares instead")
            ls_demodulator = LeastSquaresDemodulator()
            return ls_demodulator.demodulate(signal, response_matrix)

class CompressiveSensingDemodulator(BaseDemodulator):
    """
    压缩感知解调器
    """
    
    def __init__(self, sparsity=0.1):
        """
        初始化压缩感知解调器
        
        Args:
            sparsity: 稀疏度参数
        """
        self.sparsity = sparsity
    
    def demodulate(self, signal, response_matrix):
        """
        使用压缩感知解调
        
        Args:
            signal: 输入信号
            response_matrix: 响应矩阵
        
        Returns:
            解调后的光谱
        """
        try:
            import cvxpy as cp
            
            # 定义变量
            spectrum = cp.Variable(response_matrix.shape[1], nonneg=True)
            
            # 定义目标函数
            objective = cp.Minimize(cp.norm(spectrum, 1))  # L1范数
            
            # 定义约束
            constraints = [cp.norm(response_matrix @ spectrum - signal) <= self.sparsity]
            
            # 求解
            problem = cp.Problem(objective, constraints)
            problem.solve()
            
            return spectrum.value
        except ImportError:
            # 如果cvxpy不可用，使用LASSO
            print("cvxpy not available, using LASSO instead")
            lasso_demodulator = LassoDemodulator()
            return lasso_demodulator.demodulate(signal, response_matrix)
        except Exception as e:
            # 如果求解失败，使用最小二乘
            print(f"Compressive sensing failed: {e}, using least squares instead")
            ls_demodulator = LeastSquaresDemodulator()
            return ls_demodulator.demodulate(signal, response_matrix)

def demodulate(signal, response_matrix, method="least_squares", **kwargs):
    """
    解调信号的通用函数
    
    Args:
        signal: 输入信号
        response_matrix: 响应矩阵
        method: 解调方法
        **kwargs: 额外参数
    
    Returns:
        解调后的光谱
    """
    if method == "least_squares":
        demodulator = LeastSquaresDemodulator()
    elif method == "tikhonov":
        regularization = kwargs.get("reg_lambda", 0.01)
        demodulator = TikhonovDemodulator(regularization=regularization)
    elif method == "lasso":
        alpha = kwargs.get("alpha", 0.001)
        demodulator = LassoDemodulator(alpha=alpha)
    elif method == "compressive_sensing":
        sparsity = kwargs.get("sparsity", 0.1)
        demodulator = CompressiveSensingDemodulator(sparsity=sparsity)
    else:
        raise ValueError(f"Unknown demodulation method: {method}")
    
    return demodulator.demodulate(signal, response_matrix)