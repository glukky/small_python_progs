import xml.etree.ElementTree as ET
from geopy.distance import geodesic
import sys

# Убираем префиксы пространств имен в xml-документе при выводе в файл
ET.register_namespace('', 'http://www.topografix.com/GPX/1/1')

# Формируем дерево элементов
tree = ET.parse(sys.argv[1])
root = tree.getroot()

# trkseg_elem - родительские элементы для точек разделённых участков трека
# т.е. перебираем все ветви <trgseg>...</trkseg>
for trkseg_elem in root.iterfind('{*}trk/{*}trkseg'):

    # Найдём lat, lon и ele (если есть, иначе 0) первой точки участка
    trkpt_0 = trkseg_elem.find('{*}trkpt')
    latitude_0 = trkpt_0.get('lat')
    longitude_0 = trkpt_0.get('lon')
    try:
        elevation_0 = trkpt_0.find('{*}ele').text
    except AttributeError:
        elevation_0 = 0

    # Удадим из дерева элементов все точки, расстояние можду которыми
    # меньше 20м. Исключение - перепад высоты больше 1м
    for elem in trkseg_elem.findall('{*}trkpt'):
        latitude = elem.get('lat')
        longitude = elem.get('lon')
        try:
            elevation = elem.find('{*}ele').text
        except AttributeError:
            elevation = 0
        ele_delta = abs(float(elevation) - float(elevation_0))
        if ele_delta > 1:
            elevation_0 = elevation
            continue

        #Считаем расстояние между точками
        mark1 = (latitude_0, longitude_0)
        mark2 = (latitude, longitude)
        dist = geodesic(mark1, mark2, ellipsoid='WGS-84').m
        if dist < 20:
            trkseg_elem.remove(elem)
        else:
            latitude_0 = latitude
            longitude_0 = longitude
            elevation_0 = elevation

    # Возвращаем первую точку участка (dist = 0 >> алгоритм удаляет её)
    trkseg_elem.insert(0, trkpt_0)

#Записываем новый xml-документ на основе полученного дерева
file_name = sys.argv[1]
new_file_name = file_name[:-4] + '_new.gpx'
tree.write(new_file_name, encoding="UTF-8")
