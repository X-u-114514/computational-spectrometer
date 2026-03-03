"""
傅里叶变换光谱仪示例
"""

import numpy as np
import matplotlib.pyplot as plt
from computational_spectrometer.core import FourierTransformSpectrometer
from computational_spectrometer.spectrum import generate_multi_peak_spectrum
from computational_spectrometer.evaluation import PerformanceEvaluator
from computational_spectrometer.visualization import plot_spectrum_comparison

# 设置matplotlib字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建傅里叶变换光谱仪
fts = FourierTransformSpectrometer(
    wavelength_range=(400, 700),
    max_opd=1000.0,
    apodization="hann"
)

# 生成输入光谱
input_spectrum = generate_multi_peak_spectrum(
    fts.wavelengths,
    num_peaks=3,
    min_amplitude=0.5,
    max_amplitude=1.0,
    min_width=10,
    max_width=30
)

# 模拟完整链路
results = fts.simulate_full_chain(input_spectrum, demod_method="fft")

# 评估重建质量
evaluator = PerformanceEvaluator(fts.wavelengths)
metrics = evaluator.evaluate_single_reconstruction(input_spectrum, results['reconstructed'])

# 打印评估结果
print("傅里叶变换光谱仪:")
print(f"  MAE: {metrics['mae']:.4f}")
print(f"  RMSE: {metrics['rmse']:.4f}")
print(f"  相关系数: {metrics['correlation']:.4f}")
print()

# 可视化干涉图
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(fts.opd, results['signal'])
plt.title('干涉图')
plt.xlabel('光程差 (nm)')
plt.ylabel('强度')
plt.grid(True, alpha=0.3)

# 可视化重建结果
plt.subplot(1, 2, 2)
plt.plot(fts.wavelengths, input_spectrum, 'k--', label='原始光谱', linewidth=2)
plt.plot(fts.wavelengths, results['reconstructed'], 'r-', label='重建光谱', linewidth=1.5)
plt.title('重建结果')
plt.xlabel('波长 (nm)')
plt.ylabel('强度')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fts_spectrum.png', dpi=150, bbox_inches='tight')
plt.show()