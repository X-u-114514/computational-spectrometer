"""
模块5：光谱重建
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

from computational_spectrometer.evaluation import PerformanceEvaluator
from computational_spectrometer.visualization import plot_spectrum_comparison

def reconstruct_spectrum(spectrometer, input_spectrum, detected_signal):
    """
    重建光谱
    
    Args:
        spectrometer: 光谱仪实例
        input_spectrum: 输入光谱
        detected_signal: 探测器输出信号
    
    Returns:
        tuple: (重建光谱, 评估指标)
    """
    print("=== 模块5：光谱重建 ===")
    
    # 使用Tikhonov正则化解调
    reconstructed = spectrometer.demodulate(
        detected_signal,
        method="tikhonov",
        reg_lambda=0.01
    )
    
    # 评估重建质量
    evaluator = PerformanceEvaluator(spectrometer.wavelengths)
    metrics = evaluator.evaluate_single_reconstruction(input_spectrum, reconstructed)
    
    print("重建质量评估:")
    print(f"MAE: {metrics['mae']:.4f}")
    print(f"RMSE: {metrics['rmse']:.4f}")
    print(f"相关系数: {metrics['correlation']:.4f}")
    print()
    
    # 可视化重建结果
    plot_spectrum_comparison(
        spectrometer.wavelengths,
        input_spectrum,
        reconstructed,
        title="光谱重建结果",
        save_path="reconstruction_result.png"
    )
    print("重建结果图已保存为 learn1/reconstruction_result.png")
    print()
    
    return reconstructed, metrics

if __name__ == "__main__":
    # 独立运行此模块
    from spectrometer_init import init_spectrometer
    from generate_spectrum import generate_input_spectrum
    from detector_simulation import simulate_detector
    
    spectrometer = init_spectrometer()
    input_spectrum = generate_input_spectrum(spectrometer)
    detected_images, best_detected = simulate_detector(spectrometer, input_spectrum)
    reconstructed, metrics = reconstruct_spectrum(spectrometer, input_spectrum, best_detected)
    print("光谱重建完成！")