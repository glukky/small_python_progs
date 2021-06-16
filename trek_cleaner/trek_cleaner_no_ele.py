import xml.etree.ElementTree as ET
from geopy.distance import geodesic
import sys

#Убираем префиксы пространств имен в xml-документе при выводе в файл
ET.register_namespace('', 'http://www.topografix.com/GPX/1/1')

#Формируем дерево элементов
tree = ET.parse(sys.argv[1])
root = tree.getroot()

#Найдём lat, lon и ele первой точки трека
#Е - родительский элемент для всех точек трека
trkpt_0 = root.find('{*}trk/{*}trkseg/{*}trkpt')
E = root.find('{*}trk/{*}trkseg')
latitude_0 = trkpt_0.get('lat')
longitude_0 = trkpt_0.get('lon')
# elevation_0 = trkpt_0.find('{*}ele').text

# Удадим из дерева элементов все точки, расстояние можду которыми
# меньше 20м. Исключение - перепад высоты больше 1м
for elem in root.findall('{*}trk/{*}trkseg/{*}trkpt'):
    latitude = elem.get('lat')
    longitude = elem.get('lon')
#    elevation = elem.find('{*}ele').text
#    ele_delta = abs(float(elevation) - float(elevation_0))
#    if latitude == latitude_0 and longitude == longitude_0 or ele_delta > 1:
    if latitude == latitude_0 and longitude == longitude_0:
#        elevation_0 = elevation
        continue

    #Считаем расстояние между точками
    mark1 = (latitude_0, longitude_0)
    mark2 = (latitude, longitude)
    dist = geodesic(mark1, mark2, ellipsoid='WGS-84').m
    if dist < 20:
        E.remove(elem)
    else:
        latitude_0 = latitude
        longitude_0 = longitude
#        elevation_0 = elevation

#Записываем новый xml-документ на основе полученного дерева
file_name = sys.argv[1]
new_file_name = file_name[:-4] + '_new.gpx'
tree.write(new_file_name, encoding="UTF-8")
