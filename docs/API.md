# API 文档

## 核心类

### BaseSpectrometer

基础光谱仪抽象类，定义了所有光谱仪的通用接口。

**参数：**
- `wavelength_range`：波长范围 (min, max) in nm
- `num_wavelengths`：波长点数

**方法：**
- `modulate(spectrum)`：调制光谱
- `demodulate(signal, method="least_squares", **kwargs)`：解调信号
- `simulate_full_chain(spectrum, demod_method="least_squares", **kwargs)`：模拟完整的光谱仪链路

### ComputationalSpectrometer

计算光谱仪类，继承自BaseSpectrometer。

**参数：**
- `wavelength_range`：波长范围 (min, max) in nm
- `num_wavelengths`：波长点数
- `num_channels`：通道数

**属性：**
- `filter_array`：滤波器阵列
- `response_matrix`：响应矩阵

### FourierTransformSpectrometer

傅里叶变换光谱仪类，继承自BaseSpectrometer。

**参数：**
- `wavelength_range`：波长范围 (min, max) in nm
- `max_opd`：最大光程差 in nm
- `apodization`：切趾函数类型

**属性：**
- `max_opd`：最大光程差
- `apodization`：切趾函数类型
- `opd`：光程差采样点
- `apodization_function`：切趾函数

### RandomSpeckleSpectrometer

随机散斑光谱仪类，继承自BaseSpectrometer。

**参数：**
- `wavelength_range`：波长范围 (min, max) in nm
- `num_pixels`：像素数
- `speckle_size`：散斑大小
- `correlation_length`：相关长度

**属性：**
- `num_pixels`：像素数
- `speckle_size`：散斑大小
- `correlation_length`：相关长度
- `response_matrix`：响应矩阵

## 解调模块

### BaseDemodulator

基础解调器抽象类。

**方法：**
- `demodulate(signal, response_matrix)`：解调信号

### LeastSquaresDemodulator

最小二乘解调器，继承自BaseDemodulator。

**方法：**
- `demodulate(signal, response_matrix)`：使用最小二乘法解调

### TikhonovDemodulator

Tikhonov正则化解调器，继承自BaseDemodulator。

**参数：**
- `regularization`：正则化参数

**方法：**
- `demodulate(signal, response_matrix)`：使用Tikhonov正则化解调

### LassoDemodulator

LASSO解调器，继承自BaseDemodulator。

**参数：**
- `alpha`：正则化参数

**方法：**
- `demodulate(signal, response_matrix)`：使用LASSO解调

### CompressiveSensingDemodulator

压缩感知解调器，继承自BaseDemodulator。

**参数：**
- `sparsity`：稀疏度参数

**方法：**
- `demodulate(signal, response_matrix)`：使用压缩感知解调

### Calibrator

光谱仪标定器。

**参数：**
- `spectrometer`：光谱仪实例
- `num_wavelengths`：波长点数
- `num_channels`：通道数

**方法：**
- `generate_calibration_data(num_samples=21)`：生成标定数据
- `calibrate(method="direct", num_samples=21)`：执行标定

## 探测器模块

### CCDSimulator

CCD探测器模拟器。

**参数：**
- `pixels`：像素尺寸 (height, width)
- `quantum_efficiency`：量子效率
- `dark_current`：暗电流 (A/pixel)
- `read_noise`：读出噪声 (e-)

**方法：**
- `simulate(signal, exposure_time=1.0)`：模拟CCD探测器响应
- `detect_spots(image, spot_array)`：检测图像中的光斑

### SpotArray

光斑阵列类。

**参数：**
- `num_spots`：光斑数量
- `spot_size`：光斑大小

**方法：**
- `evaluate(image)`：评估光斑阵列在图像上的响应

## 评估模块

### PerformanceEvaluator

性能评估器类。

**参数：**
- `wavelengths`：波长数组

**方法：**
- `evaluate_single_reconstruction(original, reconstructed)`：评估单个重建结果
- `evaluate_multiple_reconstructions(original_spectra, reconstructed_spectra)`：评估多个重建结果

### 评估指标函数

- `calculate_mae(original, reconstructed)`：计算平均绝对误差
- `calculate_rmse(original, reconstructed)`：计算均方根误差
- `calculate_correlation(original, reconstructed)`：计算相关系数

## 光谱模块

### 光谱生成函数

- `generate_spectrum(wavelengths, peaks=None)`：生成光谱
- `generate_multi_peak_spectrum(wavelengths, num_peaks=3, min_amplitude=0.5, max_amplitude=1.0, min_width=10, max_width=30)`：生成多峰光谱

### 光谱IO函数

- `load_spectrum(file_path)`：加载光谱
- `save_spectrum(file_path, wavelengths, spectrum)`：保存光谱

## 滤波器模块

### FilterArray

滤波器阵列类。

**参数：**
- `wavelength_range`：波长范围 (min, max) in nm
- `num_wavelengths`：波长点数
- `num_filters`：滤波器数量

**方法：**
- `get_response_matrix()`：获取响应矩阵
- `get_filter_response(filter_index)`：获取单个滤波器的响应
- `visualize_filters(num_filters=5)`：可视化滤波器响应

### ModulationMatrix

调制矩阵类。

**参数：**
- `wavelength_range`：波长范围 (min, max) in nm
- `num_wavelengths`：波长点数
- `num_channels`：通道数

**方法：**
- `get_matrix()`：获取调制矩阵
- `set_matrix(matrix)`：设置调制矩阵

## 可视化模块

### 可视化函数

- `plot_spectrum(wavelengths, spectrum, title="Spectrum", xlabel="Wavelength (nm)", ylabel="Intensity", save_path=None)`：绘制光谱
- `plot_spectrum_comparison(wavelengths, original, reconstructed, title="Spectrum Comparison", xlabel="Wavelength (nm)", ylabel="Intensity", save_path=None)`：绘制光谱对比
- `plot_filter_responses(wavelengths, filter_responses, title="Filter Responses", xlabel="Wavelength (nm)", ylabel="Response", save_path=None)`：绘制滤波器响应