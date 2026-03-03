"""
总运行文件：一键运行所有模块
"""
import sys
import os

# 设置Python路径
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

# 导入所有模块
from spectrometer_init import init_spectrometer
from filter_matrix import analyze_filter_matrix
from generate_spectrum import generate_input_spectrum
from detector_simulation import simulate_detector
from spectrum_reconstruction import reconstruct_spectrum
from calibration import perform_calibration
from calibration_reconstruction import reconstruct_with_calibration
from spectrometer_comparison import compare_spectrometers

def main():
    """
    主函数：运行所有模块
    """
    print("=== 计算光谱仪仿真平台 - 完整流程 ===")
    print()
    
    # 1. 初始化光谱仪
    spectrometer = init_spectrometer()
    
    # 2. 分析滤波器矩阵
    filter_matrix = analyze_filter_matrix(spectrometer)
    
    # 3. 生成输入光谱
    input_spectrum = generate_input_spectrum(spectrometer)
    
    # 4. 模拟探测器
    detected_images, best_detected = simulate_detector(spectrometer, input_spectrum)
    
    # 5. 光谱重建
    reconstructed, metrics = reconstruct_spectrum(spectrometer, input_spectrum, best_detected)
    
    # 6. 执行标定
    calibration_matrix = perform_calibration(spectrometer)
    
    # 7. 使用标定矩阵重建
    reconstructed_cal, metrics_cal = reconstruct_with_calibration(
        spectrometer, input_spectrum, best_detected, calibration_matrix
    )
    
    # 8. 三种光谱仪对比
    comparison_metrics = compare_spectrometers(spectrometer, input_spectrum)
    
    print("=== 所有模块运行完成 ===")
    print("生成的文件:")
    print("- learn1/filter_responses.png: 滤波器响应图")
    print("- learn1/input_spectrum.png: 输入光谱图")
    print("- learn1/detector_outputs.png: 探测器输出图")
    print("- learn1/reconstruction_result.png: 重建结果图")
    print("- learn1/calibration_matrix.npy: 标定矩阵")
    print("- learn1/spectrometer_comparison.png: 三种光谱仪对比图")
    print()
    
    # 性能总结
    print("=== 性能总结 ===")
    print("计算光谱仪:")
    print(f"  MAE: {metrics['mae']:.4f}")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  相关系数: {metrics['correlation']:.4f}")
    print()
    print("使用标定矩阵:")
    print(f"  MAE: {metrics_cal['mae']:.4f}")
    print(f"  RMSE: {metrics_cal['rmse']:.4f}")
    print(f"  相关系数: {metrics_cal['correlation']:.4f}")
    print()
    print("三种光谱仪对比:")
    print(f"  计算光谱仪 - MAE: {comparison_metrics['computational']['mae']:.4f}, 相关系数: {comparison_metrics['computational']['correlation']:.4f}")
    print(f"  傅里叶变换光谱仪 - MAE: {comparison_metrics['fourier']['mae']:.4f}, 相关系数: {comparison_metrics['fourier']['correlation']:.4f}")
    print(f"  随机散斑光谱仪 - MAE: {comparison_metrics['speckle']['mae']:.4f}, 相关系数: {comparison_metrics['speckle']['correlation']:.4f}")

if __name__ == "__main__":
    main()