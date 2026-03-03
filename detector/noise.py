"""
噪声模型模块
"""

import numpy as np

def add_noise(signal, noise_type="gaussian", **kwargs):
    """
    向信号添加噪声
    
    Args:
        signal: 输入信号
        noise_type: 噪声类型
        **kwargs: 噪声参数
    
    Returns:
        带噪声的信号
    """
    if noise_type == "gaussian":
        # 高斯噪声
        mean = kwargs.get("mean", 0)
        std = kwargs.get("std", 0.01)
        noise = np.random.normal(mean, std, signal.shape)
        noisy_signal = signal + noise
    elif noise_type == "poisson":
        # 泊松噪声
        noisy_signal = np.random.poisson(signal)
    elif noise_type == "shot":
        # 散粒噪声（泊松噪声的一种）
        noisy_signal = np.random.poisson(signal)
    elif noise_type == "read":
        # 读出噪声
        std = kwargs.get("std", 10)
        noise = np.random.normal(0, std, signal.shape)
        noisy_signal = signal + noise
    else:
        raise ValueError(f"Unknown noise type: {noise_type}")
    
    # 确保非负
    noisy_signal = np.maximum(noisy_signal, 0)
    
    return noisy_signal