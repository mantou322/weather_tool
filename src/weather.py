#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
天气数据获取模块

这个模块负责从中国天气网获取天气数据，包括温度、天气状况、风力等信息。
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional


def get_weather_data_15d(city_code: str) -> Optional[Dict]:
    """获取指定城市的8-15天天气数据
    
    Args:
        city_code (str): 城市代码
    
    Returns:
        Optional[Dict]: 天气数据字典，包含以下字段：
            - date: 日期
            - high_temp: 最高气温
            - low_temp: 最低气温
            - weather: 天气状况（如：晴、雨、雪等）
            - wind_power: 风力
            如果获取失败则返回None
    """
    url = f'https://www.weather.com.cn/weather15d/{city_code}.shtml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"获取15天天气数据失败: HTTP {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        weather_div = soup.find('div', id='15d', class_='c15d')
        if not weather_div:
            print("未找到15天天气数据区域")
            return None
        
        weather_list = weather_div.find('ul', class_='t clearfix')
        if not weather_list:
            print("未找到15天天气数据列表")
            return None
        
        weather_items = weather_list.find_all('li')
        if not weather_items:
            print("未找到15天天气数据")
            return None
            
        weather_data_list = []
        
        for day_weather in weather_items[0:7]:  # 只获取第8-15天的数据
            spans = day_weather.find_all('span')
                
            # 解析日期
            date = spans[0].text if spans[0] else None
            if date:
                # 去掉最后一个字符并按（分割
                date_parts = date[:-1].split('（')
                if len(date_parts) == 2:
                    # 调换位置并添加括号
                    date = f"{date_parts[1]}（{date_parts[0]}）"
            
            # 解析天气状况
            weather = spans[1].text if spans[1] else None
            
            # 解析温度
            temp_span = spans[2]
            if temp_span:
                high_temp = temp_span.find('em').text.replace('℃', '') if temp_span.find('em') else None
                low_temp = temp_span.text.split('/')[-1].replace('℃', '') if '/' in temp_span.text else None
            else:
                high_temp = None
                low_temp = None
            
            # 确保温度数据的完整性
            if high_temp is None and low_temp is not None:
                high_temp = low_temp
            elif low_temp is None and high_temp is not None:
                low_temp = high_temp
            elif high_temp is None and low_temp is None:
                high_temp = low_temp = '0'  # 如果都为空，设置默认值为0
            
            # 解析风力
            wind_power = spans[4].text if spans[4] else None
            
            weather_data_list.append({
                'date': date,
                'high_temp': high_temp,
                'low_temp': low_temp,
                'weather': weather,
                'wind_power': wind_power
            })

        return weather_data_list
        
    except requests.RequestException as e:
        print(f"请求15天天气数据失败: {e}")
        return None
    except Exception as e:
        print(f"解析15天天气数据时出错: {e}")
        return None

def get_weather_data(city_code: str) -> Optional[Dict]:
    # 获取7天天气数据
    weather_data_7d = get_weather_data_7d(city_code)
    if not weather_data_7d:
        return None
    
    # 获取8-15天天气数据
    weather_data_15d = get_weather_data_15d(city_code)
    # print(111111111, weather_data_15d)
    if weather_data_15d:
        weather_data_7d.extend(weather_data_15d)
    
    return weather_data_7d

# 重命名原来的get_weather_data函数为get_weather_data_7d
def get_weather_data_7d(city_code: str) -> Optional[Dict]:
    """获取指定城市的7天天气数据
    
    Args:
        city_code (str): 城市代码
    
    Returns:
        Optional[Dict]: 天气数据字典，包含以下字段：
            - date: 日期
            - high_temp: 最高气温
            - low_temp: 最低气温
            - weather: 天气状况（如：晴、雨、雪等）
            - wind_power: 风力
            如果获取失败则返回None
    """
    url = f'https://www.weather.com.cn/weather/{city_code}.shtml'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 发送请求获取页面内容
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"获取天气数据失败: HTTP {response.status_code}")
            return None
        
        # 使用BeautifulSoup解析页面
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 获取天气数据
        weather_div = soup.find('div', id='7d', class_='c7d')
        if not weather_div:
            print("未找到天气数据区域")
            return None
        
        # 获取天气列表
        weather_list = weather_div.find('ul', class_='t clearfix')
        if not weather_list:
            print("未找到天气数据列表")
            return None
        
        # 获取所有天气数据
        weather_items = weather_list.find_all('li')
        if not weather_items:
            print("未找到天气数据")
            return None
            
        weather_data_list = []
        for day_weather in weather_items:
            # 解析日期
            date = day_weather.find('h1').text if day_weather.find('h1') else None
            if date:
                # 将日期格式转换为"x日（周y）"
                weekday_map = {'星期一': '周一', '星期二': '周二', '星期三': '周三',
                              '星期四': '周四', '星期五': '周五', '星期六': '周六', '星期日': '周日'}
                for full, short in weekday_map.items():
                    if full in date:
                        date = date.replace('（' + full + '）', f'（{short}）')
                        break
            
            # 解析天气状况
            weather_condition = day_weather.find('p', class_='wea')
            weather = weather_condition.get('title', weather_condition.text) if weather_condition else None
            
            # 解析温度
            temp_div = day_weather.find('p', class_='tem')
            if temp_div:
                high_temp = temp_div.find('span').text.replace('℃', '') if temp_div.find('span') else None
                low_temp = temp_div.find('i').text.replace('℃', '') if temp_div.find('i') else None
            else:
                high_temp = None
                low_temp = None
            
            # 确保温度数据的完整性
            if high_temp is None and low_temp is not None:
                high_temp = low_temp
            elif low_temp is None and high_temp is not None:
                low_temp = high_temp
            elif high_temp is None and low_temp is None:
                high_temp = low_temp = '0'  # 如果都为空，设置默认值为0
            
            # 解析风力
            wind_info = day_weather.find('p', class_='win')
            wind_power = wind_info.find('i').text if wind_info and wind_info.find('i') else None
            
            weather_data_list.append({
                'date': date,
                'high_temp': high_temp,
                'low_temp': low_temp,
                'weather': weather,
                'wind_power': wind_power
            })
        
        return weather_data_list
        
    except requests.RequestException as e:
        print(f"请求天气数据失败: {e}")
        return None
    except Exception as e:
        print(f"解析天气数据时出错: {e}")
        return None