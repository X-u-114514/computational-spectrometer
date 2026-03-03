"""
随机散斑光谱仪示例
"""

import numpy as np
import matplotlib.pyplot as plt
from computational_spectrometer.core import RandomSpeckleSpectrometer
from computational_spectrometer.spectrum import generate_multi_peak_spectrum
from computational_spectrometer.evaluation import PerformanceEvaluator
from computational_spectrometer.visualization import plot_spectrum_comparison

# 设置matplotlib字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建随机散斑光谱仪
speckle = RandomSpeckleSpectrometer(
    wavelength_range=(400, 700),
    num_pixels=256,
    speckle_size=5.0,
    correlation_length=20.0
)

# 生成输入光谱
input_spectrum = generate_multi_peak_spectrum(
    speckle.wavelengths,
    num_peaks=3,
    min_amplitude=0.5,
    max_amplitude=1.0,
    min_width=10,
    max_width=30
)

# 模拟完整链路
results = speckle.simulate_full_chain(input_spectrum, demod_method="least_squares")

# 评估重建质量
evaluator = PerformanceEvaluator(speckle.wavelengths)
metrics = evaluator.evaluate_single_reconstruction(input_spectrum, results['reconstructed'])

# 打印评估结果
print("随机散斑光谱仪:")
print(f"  MAE: {metrics['mae']:.4f}")
print(f"  RMSE: {metrics['rmse']:.4f}")
print(f"  相关系数: {metrics['correlation']:.4f}")
print()

# 可视化散斑图案
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.imshow(results['signal'].reshape(16, 16), cmap='viridis')
plt.colorbar()
plt.title('散斑图案')

# 可视化重建结果
plt.subplot(1, 2, 2)
plt.plot(speckle.wavelengths, input_spectrum, 'k--', label='原始光谱', linewidth=2)
plt.plot(speckle.wavelengths, results['reconstructed'], 'r-', label='重建光谱', linewidth=1.5)
plt.title('重建结果')
plt.xlabel('波长 (nm)')
plt.ylabel('强度')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('speckle_spectrum.png', dpi=150, bbox_inches='tight')
plt.show()