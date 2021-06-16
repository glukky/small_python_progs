import xml.etree.ElementTree as ET
from geopy.distance import geodesic
import sys


def _get_elevation(point):
    elevation_elem = point.find('{*}ele')
    if elevation_elem is not None:
        print("QQQ")
        return float(elevation_elem.text)
    return 0


_NS = 'http://www.topografix.com/GPX/1/1'


def main():
    # Убираем префиксы пространств имен в xml-документе при выводе в файл
    ET.register_namespace('g', _NS)
    ET.register_namespace('', _NS)

    # Формируем дерево элементов
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # trkseg_elem - родительские элементы для точек разделённых участков трека
    # т.е. перебираем все ветви <trgseg>...</trkseg>
    print(root)
    # for trkseg_elem in root:
    # for trkseg_elem in root.iterfind('{*}trk/{*}trkseg'):
    n = {'g': _NS}
    for trkseg_elem in root.iterfind('g:trk/g:trkseg', n):
        # if trkseg_elem.tag

        # Найдём lat, lon и ele (если есть, иначе 0) первой точки участка
        trkpt_0 = trkseg_elem.find('g:trkpt', n)
        latitude_0 = trkpt_0.get('lat')
        longitude_0 = trkpt_0.get('lon')

        elevation_0 = _get_elevation(trkpt_0)

        # Удалим из дерева элементов все точки, расстояние можду которыми
        # меньше 20м. Исключение - перепад высоты больше 1м
        for elem in trkseg_elem.findall('g:trkpt', n):
            latitude = elem.get('lat')
            longitude = elem.get('lon')

            elevation = _get_elevation(elem)

            ele_delta = abs(elevation - elevation_0)
            if ele_delta > 1:
                elevation_0 = elevation
                continue

            # Считаем расстояние между точками
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

    # Записываем новый xml-документ на основе полученного дерева
    file_name = sys.argv[1]
    new_file_name = file_name[:-4] + '_new.gpx'
    tree.write(new_file_name, encoding="UTF-8")


if __name__ == '__main__':
    main()
