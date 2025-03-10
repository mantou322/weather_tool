#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
天气工具主模块

这个模块提供了天气工具的主要功能和命令行接口。
"""

import argparse
import sys
from src import __version__
from src.city_selector import select_city, get_selected_city_code, get_selected_city_name
from src.weather import get_weather_data
from src.weather_plot import plot_weather_data


def parse_args(args):
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='天气查询工具')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    parser.add_argument(
        '-c', '--city',
        action='store_true',
        help='选择城市'
    )
    
    # 这里可以添加更多的命令行参数
    
    return parser.parse_args(args)


def main(args=None):
    """主函数"""
    if args is None:
        args = sys.argv[1:]
    
    args = parse_args(args)
    
    print("欢迎使用天气工具！")
    
    # 如果指定了--city参数或者没有指定任何参数，则启动城市选择
    if args.city or len(sys.argv) == 1:
        city_code = select_city()
        if city_code:
            print(f"已选择城市代码: {city_code}")
            # 获取并显示天气数据
            weather_data_list = get_weather_data(city_code)
            if weather_data_list:
                # print("\n未来15天天气预报:")
                # for weather_data in weather_data_list:
                #     print(f"\n{weather_data['date']}天气信息:")
                #     print(f"天气状况: {weather_data['weather']}")
                #     print(f"最高气温: {weather_data['high_temp']}℃")
                #     print(f"最低气温: {weather_data['low_temp']}℃")
                #     print(f"风力: {weather_data['wind_power']}")
                
                # 生成天气数据折线图
                print("\n正在生成天气数据折线图...")
                city_name = get_selected_city_name()
                plot_weather_data(weather_data_list, city_name)
            else:
                print("获取天气数据失败")
        else:
            print("未选择城市，退出程序")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
