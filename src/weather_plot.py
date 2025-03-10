#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
天气数据可视化模块

这个模块负责将天气数据转换为可视化图表，包括温度曲线、天气状况和风力信息。
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.font_manager as fm
import platform

def plot_weather_data(weather_data_list, city_code=None):
    """
    将天气数据绘制成折线图
    
    Args:
        weather_data_list (list): 天气数据列表，每个元素包含date、high_temp、low_temp、weather和wind_power字段
        city_code (str, optional): 城市代码
    """
    # 根据操作系统设置中文字体
    system = platform.system()
    if system == 'Windows':
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    elif system == 'Darwin':  # macOS
        plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Apple LiGothic Medium']
    else:  # Linux或其他系统
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 创建图表和坐标轴
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # 准备数据
    dates = []
    high_temps = []
    low_temps = []
    weather_info = []
    
    for data in weather_data_list:
        # 解析日期
        date_str = data['date'].split('（')[0]  # 提取日期部分
        dates.append(date_str)
        
        # 转换温度为数字并取整
        high_temps.append(int(float(data['high_temp'])))
        low_temps.append(int(float(data['low_temp'])))
        
        # 组合天气和风力信息
        weather_info.append(f"{data['weather']}\n{data['wind_power']}")
    
    # 绘制温度曲线
    ax.plot(range(len(dates)), high_temps, 'ro-', label='最高气温', linewidth=2, markersize=8)
    ax.plot(range(len(dates)), low_temps, 'bo-', label='最低气温', linewidth=2, markersize=8)
    
    # 添加温度数值标注
    for i, (high, low) in enumerate(zip(high_temps, low_temps)):
        ax.text(i, high + 1, f'{high}℃', ha='center', va='bottom')
        ax.text(i, low - 1, f'{low}℃', ha='center', va='top')
    
    # 设置x轴刻度和标签
    ax.set_xticks(range(len(dates)))
    ax.set_xticklabels(dates, rotation=45)
    
    # 添加天气和风力信息
    for i, info in enumerate(weather_info):
        ax.text(i, min(low_temps) - 5, info, ha='center', va='top', rotation=45)
    
    # 设置坐标轴标签和标题
    ax.set_xlabel('日期')
    ax.set_ylabel('温度 (°C)')
    title = '未来15天天气预报'
    if city_code:
        title = f'{city_code}未来15天天气预报'
    ax.set_title(title)
    
    # 添加图例
    ax.legend()
    
    # 调整布局
    plt.subplots_adjust(bottom=0.25)
    
    # 添加网格线
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # 显示图表
    plt.show()
    plt.close()