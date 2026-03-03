# 快速开始指南

## 基本使用

### 1. 初始化光谱仪

```python
from computational_spectrometer.core import ComputationalSpectrometer

# 创建计算光谱仪实例
spectrometer = ComputationalSpectrometer(
    wavelength_range=(400, 700),  # 波长范围 (nm)
    num_wavelengths=301,           # 波长点数
    num_channels=64                # 通道数
)
```

### 2. 生成输入光谱

```python
from computational_spectrometer.spectrum import generate_multi_peak_spectrum

# 生成多峰光谱
input_spectrum = generate_multi_peak_spectrum(
    spectrometer.wavelengths,
    num_peaks=3,
    min_amplitude=0.5,
    max_amplitude=1.0,
    min_width=10,
    max_width=30
)
```

### 3. 模拟探测器响应

```python
from computational_spectrometer.detector import CCDSimulator, SpotArray

# 生成调制信号
modulated_signal = spectrometer.modulate(input_spectrum)

# 创建CCD模拟器
ccd = CCDSimulator(pixels=(32, 32))
spot_array = SpotArray(num_spots=spectrometer.num_channels)

# 模拟探测器响应
image = ccd.simulate(modulated_signal.reshape(8, 8), exposure_time=1.0)
detected_signal = spot_array.evaluate(image)
```

### 4. 光谱重建

```python
# 使用Tikhonov正则化解调
reconstructed = spectrometer.demodulate(
    detected_signal,
    method="tikhonov",
    reg_lambda=0.01
)
```

### 5. 评估重建质量

```python
from computational_spectrometer.evaluation import PerformanceEvaluator

# 评估重建质量
evaluator = PerformanceEvaluator(spectrometer.wavelengths)
metrics = evaluator.evaluate_single_reconstruction(input_spectrum, reconstructed)

print(f"MAE: {metrics['mae']:.4f}")
print(f"RMSE: {metrics['rmse']:.4f}")
print(f"相关系数: {metrics['correlation']:.4f}")
```

## 完整示例

请参考 `learn1/run_all.py` 文件，它演示了完整的光谱仪仿真流程，包括：

1. 初始化光谱仪
2. 分析滤波器矩阵
3. 生成输入光谱
4. 模拟探测器响应
5. 光谱重建
6. 执行标定
7. 使用标定矩阵重建
8. 对比三种光谱仪性能

## 运行完整示例

```bash
python learn1/run_all.py
```

运行后，会生成以下文件：

- `learn1/filter_responses.png`：滤波器响应图
- `learn1/input_spectrum.png`：输入光谱图
- `learn1/detector_outputs.png`：探测器输出图
- `learn1/reconstruction_result.png`：重建结果图
- `learn1/calibration_matrix.npy`：标定矩阵
- `learn1/spectrometer_comparison.png`：三种光谱仪对比图

## 其他光谱仪类型

### 傅里叶变换光谱仪

```python
from computational_spectrometer.core import FourierTransformSpectrometer

# 创建傅里叶变换光谱仪实例
fts = FourierTransformSpectrometer(
    wavelength_range=(400, 700),
    max_opd=1000.0,  # 最大光程差 (nm)
    apodization="hann"  # 切趾函数
)
```

### 随机散斑光谱仪

```python
from computational_spectrometer.core import RandomSpeckleSpectrometer

# 创建随机散斑光谱仪实例
speckle = RandomSpeckleSpectrometer(
    wavelength_range=(400, 700),
    num_pixels=256,  # 像素数
    speckle_size=5.0,  # 散斑大小
    correlation_length=20.0  # 相关长度
)
```

## 解调方法

支持的解调方法：

- `least_squares`：最小二乘法
- `tikhonov`：Tikhonov正则化
- `lasso`：LASSO
- `compressive_sensing`：压缩感知

示例：

```python
# 使用LASSO解调
reconstructed = spectrometer.demodulate(
    detected_signal,
    method="lasso",
    alpha=0.001
)
```

## 标定过程

```python
from computational_spectrometer.demodulation import Calibrator

# 创建标定器
calibrator = Calibrator(spectrometer)

# 执行标定
calibration_matrix = calibrator.calibrate(method="direct")

# 使用标定矩阵重建
from computational_spectrometer.demodulation import TikhonovDemodulator
demodulator = TikhonovDemodulator(regularization=0.01)
reconstructed_cal = demodulator.demodulate(detected_signal, calibration_matrix)
```