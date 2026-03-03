"""
模块8：三种光谱仪对比
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

from computational_spectrometer.core import FourierTransformSpectrometer, RandomSpeckleSpectrometer
from computational_spectrometer.evaluation import PerformanceEvaluator

def compare_spectrometers(spectrometer, input_spectrum):
    """
    对比三种光谱仪的性能
    
    Args:
        spectrometer: 计算光谱仪实例
        input_spectrum: 输入光谱
    
    Returns:
        dict: 三种光谱仪的评估指标
    """
    print("=== 模块8：三种光谱仪对比 ===")
    
    # 傅里叶变换光谱仪
    print("测试傅里叶变换光谱仪...")
    fts = FourierTransformSpectrometer(
        wavelength_range=(400, 700),
        max_opd=1000.0,
        apodization="hann"
    )
    fts_results = fts.simulate_full_chain(input_spectrum, demod_method="fft")
    
    # 随机散斑光谱仪
    print("测试随机散斑光谱仪...")
    speckle = RandomSpeckleSpectrometer(
        wavelength_range=(400, 700),
        num_pixels=256,
        speckle_size=5.0,
        correlation_length=20.0
    )
    speckle_results = speckle.simulate_full_chain(input_spectrum, demod_method="least_squares")
    
    # 评估器
    evaluator = PerformanceEvaluator(spectrometer.wavelengths)
    
    # 评估三种光谱仪
    # 计算光谱仪的结果需要从外部传入，这里假设已经有了
    # 这里我们重新运行计算光谱仪以获取结果
    comp_results = spectrometer.simulate_full_chain(input_spectrum, demod_method="tikhonov")
    comp_metrics = evaluator.evaluate_single_reconstruction(input_spectrum, comp_results['reconstructed'])
    
    # 评估傅里叶变换光谱仪
    fts_metrics = evaluator.evaluate_single_reconstruction(input_spectrum, fts_results['reconstructed'])
    
    # 评估随机散斑光谱仪
    speckle_metrics = evaluator.evaluate_single_reconstruction(input_spectrum, speckle_results['reconstructed'])
    
    # 对比结果
    print("三种光谱仪对比结果:")
    print(f"计算光谱仪 - MAE: {comp_metrics['mae']:.4f}, 相关系数: {comp_metrics['correlation']:.4f}")
    print(f"傅里叶变换光谱仪 - MAE: {fts_metrics['mae']:.4f}, 相关系数: {fts_metrics['correlation']:.4f}")
    print(f"随机散斑光谱仪 - MAE: {speckle_metrics['mae']:.4f}, 相关系数: {speckle_metrics['correlation']:.4f}")
    print()
    
    # 可视化三种光谱仪的重建结果
    plt.figure(figsize=(12, 8))
    plt.plot(spectrometer.wavelengths, input_spectrum, 'k--', label='原始光谱', linewidth=2)
    plt.plot(spectrometer.wavelengths, comp_results['reconstructed'], 'r-', label='计算光谱仪', linewidth=1.5)
    plt.plot(fts.wavelengths, fts_results['reconstructed'], 'g-', label='傅里叶变换光谱仪', linewidth=1.5)
    plt.plot(speckle.wavelengths, speckle_results['reconstructed'], 'b-', label='随机散斑光谱仪', linewidth=1.5)
    plt.title('三种光谱仪重建结果对比')
    plt.xlabel('波长 (nm)')
    plt.ylabel('强度')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('spectrometer_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("三种光谱仪对比图已保存为 learn1/spectrometer_comparison.png")
    print()
    
    # 返回评估指标
    return {
        'computational': comp_metrics,
        'fourier': fts_metrics,
        'speckle': speckle_metrics
    }

if __name__ == "__main__":
    # 独立运行此模块
    from spectrometer_init import init_spectrometer
    from generate_spectrum import generate_input_spectrum
    
    spectrometer = init_spectrometer()
    input_spectrum = generate_input_spectrum(spectrometer)
    metrics = compare_spectrometers(spectrometer, input_spectrum)
    print("三种光谱仪对比完成！")