"""
可视化工具
"""

import matplotlib.pyplot as plt

# 设置matplotlib字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def plot_spectrum(wavelengths, spectrum, title="Spectrum", xlabel="Wavelength (nm)", ylabel="Intensity", save_path=None):
    """
    绘制光谱
    
    Args:
        wavelengths: 波长数组
        spectrum: 光谱数组
        title: 标题
        xlabel: x轴标签
        ylabel: y轴标签
        save_path: 保存路径
    """
    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, spectrum)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()

def plot_spectrum_comparison(wavelengths, original, reconstructed, title="Spectrum Comparison", xlabel="Wavelength (nm)", ylabel="Intensity", save_path=None):
    """
    绘制光谱对比
    
    Args:
        wavelengths: 波长数组
        original: 原始光谱
        reconstructed: 重建光谱
        title: 标题
        xlabel: x轴标签
        ylabel: y轴标签
        save_path: 保存路径
    """
    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, original, 'k--', label='Original', linewidth=2)
    plt.plot(wavelengths, reconstructed, 'r-', label='Reconstructed', linewidth=1.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()

def plot_filter_responses(wavelengths, filter_responses, title="Filter Responses", xlabel="Wavelength (nm)", ylabel="Response", save_path=None):
    """
    绘制滤波器响应
    
    Args:
        wavelengths: 波长数组
        filter_responses: 滤波器响应矩阵
        title: 标题
        xlabel: x轴标签
        ylabel: y轴标签
        save_path: 保存路径
    """
    plt.figure(figsize=(10, 6))
    for i, response in enumerate(filter_responses):
        plt.plot(wavelengths, response, label=f'Filter {i+1}')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()