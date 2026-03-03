"""
模块2：滤波器矩阵查看和可视化
"""
import sys
import os
import matplotlib.pyplot as plt

# 设置Python路径
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

# 设置matplotlib字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def analyze_filter_matrix(spectrometer):
    """
    分析和可视化滤波器矩阵
    
    Args:
        spectrometer: 光谱仪实例
    
    Returns:
        numpy.ndarray: 滤波器矩阵
    """
    print("=== 模块2：分析滤波器矩阵 ===")
    
    # 获取滤波器矩阵
    filter_matrix = spectrometer.response_matrix
    print(f"滤波器矩阵形状: {filter_matrix.shape}")
    
    # 可视化前5个滤波器的响应
    print("可视化前5个滤波器的响应...")
    plt.figure(figsize=(10, 6))
    for i in range(5):
        plt.plot(spectrometer.wavelengths, filter_matrix[i], label=f'通道 {i+1}')
    plt.title('滤波器响应')
    plt.xlabel('波长 (nm)')
    plt.ylabel('响应')
    plt.legend()
    plt.savefig('filter_responses.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("滤波器响应图已保存为 learn1/filter_responses.png")
    print()
    
    return filter_matrix

if __name__ == "__main__":
    # 独立运行此模块
    from spectrometer_init import init_spectrometer
    spectrometer = init_spectrometer()
    filter_matrix = analyze_filter_matrix(spectrometer)
    print("滤波器矩阵分析完成！")