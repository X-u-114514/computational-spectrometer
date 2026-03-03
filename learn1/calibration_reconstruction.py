"""
模块7：使用标定矩阵重建
"""
import sys
import os
import numpy as np

# 设置Python路径
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

from computational_spectrometer.evaluation import PerformanceEvaluator
from computational_spectrometer.demodulation import TikhonovDemodulator

def reconstruct_with_calibration(spectrometer, input_spectrum, detected_signal, calibration_matrix):
    """
    使用标定矩阵重建光谱
    
    Args:
        spectrometer: 光谱仪实例
        input_spectrum: 输入光谱
        detected_signal: 探测器输出信号
        calibration_matrix: 标定矩阵
    
    Returns:
        tuple: (重建光谱, 评估指标)
    """
    print("=== 模块7：使用标定矩阵重建 ===")
    
    # 创建解调器
    demodulator = TikhonovDemodulator(regularization=0.01)
    
    # 使用标定矩阵重建
    reconstructed_cal = demodulator.demodulate(detected_signal, calibration_matrix)
    
    # 评估使用标定矩阵的重建质量
    evaluator = PerformanceEvaluator(spectrometer.wavelengths)
    metrics_cal = evaluator.evaluate_single_reconstruction(input_spectrum, reconstructed_cal)
    
    print("使用标定矩阵的重建质量:")
    print(f"MAE: {metrics_cal['mae']:.4f}")
    print(f"RMSE: {metrics_cal['rmse']:.4f}")
    print(f"相关系数: {metrics_cal['correlation']:.4f}")
    print()
    
    return reconstructed_cal, metrics_cal

if __name__ == "__main__":
    # 独立运行此模块
    from spectrometer_init import init_spectrometer
    from generate_spectrum import generate_input_spectrum
    from detector_simulation import simulate_detector
    from calibration import perform_calibration
    
    spectrometer = init_spectrometer()
    input_spectrum = generate_input_spectrum(spectrometer)
    detected_images, best_detected = simulate_detector(spectrometer, input_spectrum)
    calibration_matrix = perform_calibration(spectrometer)
    reconstructed_cal, metrics_cal = reconstruct_with_calibration(spectrometer, input_spectrum, best_detected, calibration_matrix)
    print("使用标定矩阵重建完成！")