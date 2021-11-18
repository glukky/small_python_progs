import os
import sys

import xml.etree.ElementTree as ET
from geopy import distance as gd


_DISTANCE_TRESHOLD = 20

_NS = 'http://www.topografix.com/GPX/1/1'


def _get_elevation(point):
    elevation_elem = point.find('{*}ele')
    if elevation_elem is not None:
        return float(elevation_elem.text)
    return 0


def main():
    ET.register_namespace('g', _NS)
    ET.register_namespace('', _NS)

    if len(sys.argv) < 3:
        print("Usage: trek_cleaner.py <input_track.gpx> <output_track.gpx>")
        sys.exit(1)

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    if not os.path.exists(input_file_name):
        print("Error: File `{}` not found".format(input_file_name))
        sys.exit(2)

    tree = ET.parse(input_file_name)
    root = tree.getroot()

    # trkseg_elem - родительские элементы для точек разделённых участков трека
    # т.е. перебираем все ветви <trgseg>...</trkseg>

    ns = {'g': _NS}
    for trkseg_elem in root.iterfind('g:trk/g:trkseg', ns):

        # Найдём lat, lon и ele (если есть, иначе 0) первой точки участка
        trkpt_prev = trkseg_elem.find('g:trkpt', ns)
        latitude_prev = trkpt_prev.get('lat')
        longitude_prev = trkpt_prev.get('lon')

        elevation_prev = _get_elevation(trkpt_prev)

        # Удалим из дерева элементов все точки, расстояние можду которыми
        # меньше 20м. Исключение - перепад высоты больше 1м
        first = True
        for elem in trkseg_elem.findall('g:trkpt', ns):
            if first:
                # пропускаем первую точку
                first = False
                continue

            latitude = elem.get('lat')
            longitude = elem.get('lon')
            elevation = _get_elevation(elem)

            elevation_delta = abs(elevation - elevation_prev)
            if elevation_delta > 1:
                elevation_prev = elevation
                continue

            # Считаем расстояние между точками
            mark1 = latitude_prev, longitude_prev
            mark2 = latitude, longitude
            distance = gd.geodesic(mark1, mark2, ellipsoid='WGS-84').m
            if distance < _DISTANCE_TRESHOLD:
                trkseg_elem.remove(elem)
            else:
                latitude_prev = latitude
                longitude_prev = longitude
                elevation_prev = elevation

    # Записываем новый xml-документ на основе полученного дерева
    tree.write(output_file_name, encoding="UTF-8")


if __name__ == '__main__':
    main()
