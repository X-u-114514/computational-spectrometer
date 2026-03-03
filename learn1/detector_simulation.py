"""
模块4：探测器模拟
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# 设置Python路径
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

# 设置matplotlib字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def simulate_detector(spectrometer, input_spectrum):
    """
    模拟探测器响应
    
    Args:
        spectrometer: 光谱仪实例
        input_spectrum: 输入光谱
    
    Returns:
        tuple: (探测器输出图像列表, 最佳探测器输出)
    """
    print("=== 模块4：探测器模拟 ===")
    
    # 生成调制信号
    modulated_signal = spectrometer.modulate(input_spectrum)
    
    # 创建CCD模拟器
    from computational_spectrometer.detector import CCDSimulator, SpotArray
    ccd = CCDSimulator(pixels=(32, 32))
    spot_array = SpotArray(num_spots=spectrometer.num_channels)
    
    # 模拟不同曝光时间
    exposure_times = [0.1, 0.5, 1.0]
    detected_images = []
    best_detected = None
    best_exp_time = 0
    
    print("模拟不同曝光时间...")
    for exp_time in exposure_times:
        # 模拟探测器响应
        image = ccd.simulate(modulated_signal.reshape(8, 8), exposure_time=exp_time)
        detected_images.append(image)
        
        # 检测光斑
        detected = spot_array.evaluate(image)
        
        # 计算均值和最大值
        mean_val = np.mean(detected)
        max_val = np.max(detected)
        print(f"曝光时间 {exp_time}s: 均值 = {mean_val:.2f}, 最大值 = {max_val:.2f}")
        
        # 选择最佳曝光时间（均值在0.1-0.8之间）
        if 0.1 <= mean_val <= 0.8 and (best_detected is None or mean_val > np.mean(best_detected)):
            best_detected = detected
            best_exp_time = exp_time
    
    # 如果没有找到合适的曝光时间，使用最后一个
    if best_detected is None:
        best_detected = spot_array.evaluate(detected_images[-1])
        best_exp_time = exposure_times[-1]
    
    print(f"选择最佳曝光时间: {best_exp_time}s")
    
    # 可视化探测器输出
    plt.figure(figsize=(12, 4))
    for i, (image, exp_time) in enumerate(zip(detected_images, exposure_times)):
        plt.subplot(1, 3, i+1)
        im = plt.imshow(image, cmap='viridis')
        plt.colorbar(im)
        plt.title(f'曝光时间: {exp_time}s')
    plt.tight_layout()
    plt.savefig('detector_outputs.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("探测器输出图已保存为 learn1/detector_outputs.png")
    print()
    
    return detected_images, best_detected

if __name__ == "__main__":
    # 独立运行此模块
    from spectrometer_init import init_spectrometer
    from generate_spectrum import generate_input_spectrum
    
    spectrometer = init_spectrometer()
    input_spectrum = generate_input_spectrum(spectrometer)
    detected_images, best_detected = simulate_detector(spectrometer, input_spectrum)
    print("探测器模拟完成！")