import xml.etree.ElementTree as ET
from geopy.distance import geodesic
import sys

def _get_elevation(point):
    elevation_elem = point.find('{*}ele')
    if elevation_elem is not None:
#        print("QQQ")
        return float(elevation_elem.text)
    return 0

_NS = 'http://www.topografix.com/GPX/1/1'

def main():
    # Убираем префиксы пространств имен в xml-документе при выводе в файл
    ET.register_namespace('', 'http://www.topografix.com/GPX/1/1')
    n = {'g': _NS}

    # Формируем два идентичных дерева элементов
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    cut_tree = ET.parse(sys.argv[1])
    cut_root = cut_tree.getroot()

    # Вырезаем из дерева cut_tree все элементы trkpt
    for trkseg_elem in cut_root.iterfind('g:trk/g:trkseg', n):
        for elem in trkseg_elem.findall('g:trkpt', n):
            trkseg_elem.remove(elem)

    # Находим элемент trk в root и запоминаем его индекс
    for index in range(len(root)):
        elem = root[index]
    #    print(elem.tag)
        if elem.tag == '{' + _NS + '}' + 'trk':
            x = index
    #        print('x=', x)

    # Переберем в цикле все подэлементы trk
    for index in range(len(root[x])):
        elem = root[x][index]
    #    print(elem.tag)

        # И проверим, являются ли они trkseg
        if elem.tag == '{' + _NS + '}' + 'trkseg':
    #        print('!')

            # Положим в каждый сегмент trkseg его первую точку (из tree в cut_tree)
            trkpt_0 = elem.find('g:trkpt', n)
            cut_trkseg = cut_root[x][index]
            cut_trkseg.append(trkpt_0)

            # Заполняем cut_tree точками на расстоянии не менее 40м
            # Сначала вычислим расстояние между соседними точками участка trkseg в tree

            # Найдём lat, lon и ele (если есть, иначе 0) первой точки участка
            latitude_0 = trkpt_0.get('lat')
            longitude_0 = trkpt_0.get('lon')

            elevation_0 = _get_elevation(trkpt_0)

            # Переберем в цикле остальные точки в участках trksek, запоминая координаты
            for index_pt in range(1, len(elem)):
                checked_trkpt = elem[index_pt]
                latitude = checked_trkpt.get('lat')
                longitude = checked_trkpt.get('lon')

                elevation = _get_elevation(checked_trkpt)

                # Считаем расстояние между точками
                mark1 = (latitude_0, longitude_0)
                mark2 = (latitude, longitude)
                dist = geodesic(mark1, mark2, ellipsoid='WGS-84').m

                # Если точка удалена на 40м от последней в cut_tree, добавляем её туда же
                # Иначе игнорируем и рассчитываем следующую точку сегмента trkseg
                if dist >= 40:
                    cut_trkseg.append(checked_trkpt)

                    # Перекладываем запоминалки о последнее точке
                    latitude_0 = latitude
                    longitude_0 = longitude
                    elevation_0 = elevation


    #Записываем новый xml-документ на основе полученного дерева cut_tree
    file_name = sys.argv[1]
    new_file_name = file_name[:-4] + '_new.gpx'
    cut_tree.write(new_file_name, encoding="UTF-8")

    print('File', new_file_name, 'was successfully created')


if __name__ == '__main__':
    main()