"""数据分析处理"""
import time
from math import ceil
from pprint import pprint

import branca
from numpy import ndarray

from database import GetData
import pandas as pd
import folium

groups_dict = {}
earthquakedata_list = list(GetData(TableName="earthquakedata"))
DFdata = pd.DataFrame(earthquakedata_list)


def formatdata():
    """
    把从数据库中获取出来的数据进行分组处理，并进行格式化
    :return: groups_dict
    """
    groups = DFdata.groupby("LOCATION_C").groups
    for item in groups.items():
        groups_dict[item[0]] = item[-1].tolist()
    return groups_dict


def getcoordinate(objects: dict):
    """
    获取坐标点
    :param objects:格式化后的数据
    :return: 地点及各地点的坐标
    """
    coordinate = {}
    for key, value in objects.items():
        LAT = []  # 维度
        LON = []  # 经度
        for index in value:
            LAT.append(float(DFdata['EPI_LAT'][index]))
            LON.append(float(DFdata['EPI_LON'][index]))
        coordinate[key] = [sum(LAT) / len(LAT), sum(LON) / len(LON)]
    return coordinate


def getfrequency():
    """
    获取每个地方的地震次数
    :return:{地区：次数}
    """
    frequency = DFdata["LOCATION_C"].value_counts()
    return dict(frequency)


def selectlabel(count: int):
    """
    通过不同的地震次数定制标签
    :param count: 地震次数
    :return: 包含标签颜色及样式的字典
    """
    label_dict = {}
    color_set = {1: 'gray', 2: 'green', 3: 'blue', 4: 'red', 5: 'darkred'}
    lable_set = {1: 'star-o', 2: 'star-half-o', 3: 'star'}
    color_count = ceil(count / 45)
    lable_count = ceil((count - (45 * (color_count - 1))) / 15)
    label_dict['color'] = color_set[color_count]
    label_dict['lable'] = lable_set[lable_count]
    return label_dict


def visua(coordinate: dict, frequency: dict):
    """
    可视化图表并生成HTML文件
    folium.Marker(
        location：经纬度列表
        popup：点击标记点时弹出的内容
        tooltip：鼠标移动到标记点时弹出的提示
        icon：标记点颜色)
    :param coordinate:
    :return:
    """
    world_map = folium.Map(location=None, width="100%", height="100%", left='0%', top='0%',
                           position='relative', tiles='OpenStreetMap', attr=None, min_zoom=2.5, max_zoom=18,
                           zoom_start=1000, min_lat=-90, max_lat=90, min_lon=-180, max_lon=180, max_bounds=False,
                           crs='EPSG3857', control_scale=False, prefer_canvas=False, no_touch=False, disable_3d=False,
                           png_enabled=False, zoom_control=True)
    for key, value in coordinate.items():
        count = frequency[key]
        label_dict = selectlabel(count)
        folium.Marker(
            location=tuple(value),
            popup=folium.Popup(str(count), max_width=100),
            tooltip=str(key),
            icon=folium.Icon(color=label_dict['color'], prefix='fa', icon=label_dict['lable']),
            draggable=False,
        ).add_to(world_map)
    world_map.save("world_map.html")


if __name__ == "__main__":
    while True:
        time_now = time.strftime("%H:%M:%S", time.localtime())  # 刷新
        if time_now == "01:00:00":
            data = formatdata()
            coordinate = getcoordinate(objects=data)
            frequency = getfrequency()
            visua(coordinate=coordinate, frequency=frequency)
            time.sleep(60)
