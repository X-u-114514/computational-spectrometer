"""
模块3：生成输入光谱
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

def generate_input_spectrum(spectrometer):
    """
    生成输入光谱
    
    Args:
        spectrometer: 光谱仪实例
    
    Returns:
        numpy.ndarray: 输入光谱
    """
    print("=== 模块3：生成输入光谱 ===")
    
    # 生成多峰光谱
    from computational_spectrometer.spectrum import generate_multi_peak_spectrum
    input_spectrum = generate_multi_peak_spectrum(
        spectrometer.wavelengths,
        num_peaks=3,
        min_amplitude=0.5,
        max_amplitude=1.0,
        min_width=10,
        max_width=30
    )
    
    # 可视化输入光谱
    plt.figure(figsize=(10, 6))
    plt.plot(spectrometer.wavelengths, input_spectrum)
    plt.title('输入光谱')
    plt.xlabel('波长 (nm)')
    plt.ylabel('强度')
    plt.savefig('input_spectrum.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("输入光谱图已保存为 learn1/input_spectrum.png")
    print()
    
    return input_spectrum

if __name__ == "__main__":
    # 独立运行此模块
    from spectrometer_init import init_spectrometer
    spectrometer = init_spectrometer()
    input_spectrum = generate_input_spectrum(spectrometer)
    print("输入光谱生成完成！")