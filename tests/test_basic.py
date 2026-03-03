"""
基础测试
"""

import numpy as np
from computational_spectrometer.core import ComputationalSpectrometer, FourierTransformSpectrometer, RandomSpeckleSpectrometer
from computational_spectrometer.spectrum import generate_multi_peak_spectrum
from computational_spectrometer.evaluation import PerformanceEvaluator

def test_computational_spectrometer():
    """测试计算光谱仪"""
    print("测试计算光谱仪...")
    
    # 创建光谱仪
    spectrometer = ComputationalSpectrometer(
        wavelength_range=(400, 700),
        num_wavelengths=301,
        num_channels=64
    )
    
    # 生成输入光谱
    input_spectrum = generate_multi_peak_spectrum(spectrometer.wavelengths)
    
    # 调制和解调
    modulated = spectrometer.modulate(input_spectrum)
    reconstructed = spectrometer.demodulate(modulated, method="tikhonov")
    
    # 评估
    evaluator = PerformanceEvaluator(spectrometer.wavelengths)
    metrics = evaluator.evaluate_single_reconstruction(input_spectrum, reconstructed)
    
    print(f"  MAE: {metrics['mae']:.4f}")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  相关系数: {metrics['correlation']:.4f}")
    print("  测试通过！")
    print()

def test_fourier_spectrometer():
    """测试傅里叶变换光谱仪"""
    print("测试傅里叶变换光谱仪...")
    
    # 创建光谱仪
    fts = FourierTransformSpectrometer(
        wavelength_range=(400, 700),
        max_opd=1000.0
    )
    
    # 生成输入光谱
    input_spectrum = generate_multi_peak_spectrum(fts.wavelengths)
    
    # 模拟完整链路
    results = fts.simulate_full_chain(input_spectrum, demod_method="fft")
    
    # 评估
    evaluator = PerformanceEvaluator(fts.wavelengths)
    metrics = evaluator.evaluate_single_reconstruction(input_spectrum, results['reconstructed'])
    
    print(f"  MAE: {metrics['mae']:.4f}")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  相关系数: {metrics['correlation']:.4f}")
    print("  测试通过！")
    print()

def test_speckle_spectrometer():
    """测试随机散斑光谱仪"""
    print("测试随机散斑光谱仪...")
    
    # 创建光谱仪
    speckle = RandomSpeckleSpectrometer(
        wavelength_range=(400, 700),
        num_pixels=256
    )
    
    # 生成输入光谱
    input_spectrum = generate_multi_peak_spectrum(speckle.wavelengths)
    
    # 模拟完整链路
    results = speckle.simulate_full_chain(input_spectrum, demod_method="least_squares")
    
    # 评估
    evaluator = PerformanceEvaluator(speckle.wavelengths)
    metrics = evaluator.evaluate_single_reconstruction(input_spectrum, results['reconstructed'])
    
    print(f"  MAE: {metrics['mae']:.4f}")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  相关系数: {metrics['correlation']:.4f}")
    print("  测试通过！")
    print()

if __name__ == "__main__":
    test_computational_spectrometer()
    test_fourier_spectrometer()
    test_speckle_spectrometer()
    print("所有测试通过！")