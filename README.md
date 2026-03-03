# 计算光谱仪通用仿真平台

## 项目简介

计算光谱仪通用仿真平台是一个用于模拟和评估不同类型光谱仪性能的开源软件框架。该平台支持三种主要的光谱仪架构：

- **计算光谱仪**：基于可编程滤波器阵列的光谱仪
- **傅里叶变换光谱仪**：基于干涉原理的光谱仪
- **随机散斑光谱仪**：基于随机散射的光谱仪

## 功能特性

- **完整的光谱仪模型**：包含光源、光学系统、探测器和数据处理模块
- **多种解调算法**：支持最小二乘法、Tikhonov正则化、LASSO和压缩感知
- **探测器噪声模型**：模拟CCD噪声、暗电流和读出噪声
- **标定流程**：完整的光谱仪标定过程
- **性能评估**：使用MAE、RMSE和相关系数评估重建质量
- **模块化设计**：便于扩展和定制

## 目录结构

```
computational_spectrometer/
├── core/             # 核心光谱仪实现
├── demodulation/     # 解调算法
├── detector/         # 探测器模型
├── evaluation/       # 性能评估
├── filters/          # 滤波器设计
├── spectrum/         # 光谱生成和处理
├── visualization/    # 可视化工具
├── examples/         # 示例代码
├── tests/            # 测试代码
└── learn1/           # 学习示例模块
```

## 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/X-u-114514/computational-spectrometer.git
   cd computational-spectrometer
   ```

2. 安装依赖：
   ```bash
   pip install -e .
   ```

3. 运行示例：
   ```bash
   python learn1/run_all.py
   ```

## 快速开始

请参考 `docs/QUICKSTART.md` 文件获取详细的使用指南。

## 许可证

本项目采用MIT许可证。