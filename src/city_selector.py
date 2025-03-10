#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
城市选择模块

这个模块提供了基于city_code.json文件的三级城市选择功能，
允许用户选择省份、城市和区县，并获取对应的城市代码。
"""

import json
import os
from pathlib import Path

# 全局变量，用于存储选择的城市代码和城市名称
selected_city_code = None
selected_city_name = None

def load_city_data():
    """
    加载城市数据文件
    
    Returns:
        dict: 包含所有城市数据的字典
    """
    # 获取city_code.json文件的绝对路径
    data_dir = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / 'data'
    city_file = data_dir / 'city_code.json'
    
    try:
        with open(city_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载城市数据失败: {e}")
        return None

def display_menu(items, title="请选择"):
    """
    显示选择菜单
    
    Args:
        items (list): 要显示的选项列表
        title (str): 菜单标题
        
    Returns:
        int: 用户选择的索引，如果输入无效则返回-1
    """
    print(f"\n{title}:")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item['name']}")
    
    try:
        choice = int(input("请输入选项编号: "))
        if 1 <= choice <= len(items):
            return choice - 1
        else:
            print("无效的选择，请输入有效的编号。")
            return -1
    except ValueError:
        print("请输入数字。")
        return -1

def select_city():
    """三级城市选择功能
    
    Returns:
        str: 选择的城市代码，如果选择失败则返回None
    """
    global selected_city_code, selected_city_name
    
    # 加载城市数据
    city_data = load_city_data()
    if not city_data:
        return None
    
    # 获取省份列表
    provinces = city_data.get('zone', [])
    if not provinces:
        print("未找到省份数据")
        return None
    
    # 默认选择辽宁省（索引22）
    default_province_idx = 22
    print(f"默认选择: {provinces[default_province_idx]['name']}")
    province_idx = display_menu(provinces, "请选择省份（直接回车选择默认值）")
    if province_idx == -1:
        province_idx = default_province_idx
        print(f"已选择默认值: {provinces[province_idx]['name']}")
    
    # 获取选中省份的城市列表
    cities = provinces[province_idx].get('zone', [])
    if not cities:
        print(f"未找到 {provinces[province_idx]['name']} 的城市数据")
        return None
    
    # 默认选择沈阳市（索引13）
    default_city_idx = 13 if province_idx == default_province_idx else 0
    print(f"默认选择: {cities[default_city_idx]['name']}")
    city_idx = display_menu(cities, "请选择城市（直接回车选择默认值）")
    if city_idx == -1:
        city_idx = default_city_idx
        print(f"已选择默认值: {cities[city_idx]['name']}")
    
    # 获取选中城市的区县列表
    districts = cities[city_idx].get('zone', [])
    if not districts:
        print(f"未找到 {cities[city_idx]['name']} 的区县数据")
        return None
    
    # 默认选择沈阳（索引2）
    default_district_idx = 2 if province_idx == default_province_idx and city_idx == default_city_idx else 0
    print(f"默认选择: {districts[default_district_idx]['name']}")
    district_idx = display_menu(districts, "请选择区县（直接回车选择默认值）")
    if district_idx == -1:
        district_idx = default_district_idx
        print(f"已选择默认值: {districts[district_idx]['name']}")
    
    # 获取选中区县的城市代码和名称
    selected_city_code = districts[district_idx].get('code')
    selected_city_name = districts[district_idx].get('name')
    if not selected_city_code:
        print(f"未找到 {districts[district_idx]['name']} 的城市代码")
        return None
    
    print(f"\n已选择: {provinces[province_idx]['name']} > {cities[city_idx]['name']} > {districts[district_idx]['name']}")
    print(f"城市代码: {selected_city_code}")
    
    return selected_city_code

def get_selected_city_code():
    """
    获取当前选择的城市代码
    
    Returns:
        str: 当前选择的城市代码，如果未选择则返回None
    """
    global selected_city_code
    return selected_city_code

def set_selected_city_code(code):
    """
    设置当前选择的城市代码
    
    Args:
        code (str): 要设置的城市代码
    """
    global selected_city_code
    selected_city_code = code

def get_selected_city_name():
    """获取当前选择的城市名称
    
    Returns:
        str: 当前选择的城市名称，如果未选择则返回None
    """
    global selected_city_name
    return selected_city_name

def set_selected_city_name(name):
    """设置当前选择的城市名称
    
    Args:
        name (str): 要设置的城市名称
    """
    global selected_city_name
    selected_city_name = name