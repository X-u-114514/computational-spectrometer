"""
计算光谱仪通用仿真平台 - 安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="computational-spectrometer",
    version="1.0.0",
    author="Computational Spectrometer Team",
    author_email="",
    description="计算光谱仪通用仿真平台",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "full": ["cvxpy>=1.2.0", "plotly>=5.0.0", "h5py>=3.0.0"],
        "dev": ["pytest>=6.0.0", "black>=21.0", "flake8>=3.9.0"],
    },
    entry_points={
        "console_scripts": [
            "comp-spec=computational_spectrometer.cli:main",
        ],
    },
)