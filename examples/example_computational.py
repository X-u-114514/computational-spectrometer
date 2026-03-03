"""
计算光谱仪示例
"""

import numpy as np
import matplotlib.pyplot as plt
from computational_spectrometer.core import ComputationalSpectrometer
from computational_spectrometer.spectrum import generate_multi_peak_spectrum
from computational_spectrometer.evaluation import PerformanceEvaluator
from computational_spectrometer.visualization import plot_spectrum_comparison

# 设置matplotlib字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建计算光谱仪
spectrometer = ComputationalSpectrometer(
    wavelength_range=(400, 700),
    num_wavelengths=301,
    num_channels=64
)

# 生成输入光谱
input_spectrum = generate_multi_peak_spectrum(
    spectrometer.wavelengths,
    num_peaks=3,
    min_amplitude=0.5,
    max_amplitude=1.0,
    min_width=10,
    max_width=30
)

# 调制光谱
modulated_signal = spectrometer.modulate(input_spectrum)

# 解调光谱（使用不同方法）
reconstructed_ls = spectrometer.demodulate(modulated_signal, method="least_squares")
reconstructed_tikhonov = spectrometer.demodulate(modulated_signal, method="tikhonov", reg_lambda=0.01)
reconstructed_lasso = spectrometer.demodulate(modulated_signal, method="lasso", alpha=0.001)

# 评估重建质量
evaluator = PerformanceEvaluator(spectrometer.wavelengths)
metrics_ls = evaluator.evaluate_single_reconstruction(input_spectrum, reconstructed_ls)
metrics_tikhonov = evaluator.evaluate_single_reconstruction(input_spectrum, reconstructed_tikhonov)
metrics_lasso = evaluator.evaluate_single_reconstruction(input_spectrum, reconstructed_lasso)

# 打印评估结果
print("最小二乘法:")
print(f"  MAE: {metrics_ls['mae']:.4f}")
print(f"  RMSE: {metrics_ls['rmse']:.4f}")
print(f"  相关系数: {metrics_ls['correlation']:.4f}")
print()

print("Tikhonov正则化:")
print(f"  MAE: {metrics_tikhonov['mae']:.4f}")
print(f"  RMSE: {metrics_tikhonov['rmse']:.4f}")
print(f"  相关系数: {metrics_tikhonov['correlation']:.4f}")
print()

print("LASSO:")
print(f"  MAE: {metrics_lasso['mae']:.4f}")
print(f"  RMSE: {metrics_lasso['rmse']:.4f}")
print(f"  相关系数: {metrics_lasso['correlation']:.4f}")
print()

# 可视化结果
plt.figure(figsize=(12, 8))
plt.plot(spectrometer.wavelengths, input_spectrum, 'k--', label='原始光谱', linewidth=2)
plt.plot(spectrometer.wavelengths, reconstructed_ls, 'r-', label='最小二乘法', linewidth=1.5)
plt.plot(spectrometer.wavelengths, reconstructed_tikhonov, 'g-', label='Tikhonov正则化', linewidth=1.5)
plt.plot(spectrometer.wavelengths, reconstructed_lasso, 'b-', label='LASSO', linewidth=1.5)
plt.title('不同解调方法的重建结果')
plt.xlabel('波长 (nm)')
plt.ylabel('强度')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('computational_spectrum.png', dpi=150, bbox_inches='tight')
plt.show()