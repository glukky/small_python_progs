import xml.etree.ElementTree as ET
from geopy.distance import geodesic
import sys

def _get_elevation(point):
    elevation_elem = point.find('{*}ele')
    if elevation_elem is not None:
    #    print("QQQ")
        return float(elevation_elem.text)
    return 0

_NS = 'http://www.topografix.com/GPX/1/1'

def main():
    n = {'g': _NS}

    # Формируем дерево элементов
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    dist_all = 0
    ascent = 0
    descent = 0


    # Пусть максимальная высота сначала равна высоте первой точки трека
    elevation_max = _get_elevation(root.find('g:trk/g:trkseg/g:trkpt/', n))

    # Задача перебрать все ветви <trgseg>...</trkseg> и обработать данные точек

    # Находим элемент trk в root и запоминаем его индекс х
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

            # Если это trkseg, запомним его первую точку
            trkpt_0 = elem.find('g:trkpt', n)

            # Найдём lat, lon и ele (если есть, иначе 0) первой точки участка
            latitude_0 = trkpt_0.get('lat')
            longitude_0 = trkpt_0.get('lon')

            elevation_0 = _get_elevation(trkpt_0)
            elev_0 = float(elevation_0)

            # Выберем новую макс высоту, если первая точка участка выше elevation_max
            if elev_0 > elevation_max:
                elevation_max = elev_0


            # Зададим набор и сброс на участке равными нулю
            ascent_seg = 0
            descent_seg = 0

            # Переберем остальные точки участка, запомним их lat, lon, ele
            for index_pt in range(1, len(elem)):
                checked_trkpt = elem[index_pt]
                latitude = checked_trkpt.get('lat')
                longitude = checked_trkpt.get('lon')

                elevation = _get_elevation(checked_trkpt)

                # Считаем расстояние между точками
                mark1 = (latitude_0, longitude_0)
                mark2 = (latitude, longitude)
                dist = geodesic(mark1, mark2, ellipsoid='WGS-84').m

                # Добавляем расстояние к общему
                dist_all += dist

                # Вычисляем изменение высоты, перекладываем данные новой точки в предыдущие запоминалки
                ele_delta = float(elevation) - float(elevation_0)
                latitude_0 = latitude
                longitude_0 = longitude
                elevation_0 = elevation
                elev = float(elevation)

                # Набор и сброс подсчитываем раздельно
                if ele_delta > 0:
                    ascent_seg += ele_delta
                else:
                    descent_seg += ele_delta

                # Запомним новую макс высоту на участке trkseg, если найдем
                if elev > elevation_max:
                    elevation_max = elev

            # Если элемент был trkseg, добавляем его сброс и набор к общим
            ascent += ascent_seg
            descent += descent_seg

    print('Дистанция трека:', round(dist_all / 1000, 2), 'км')
    print('Максимальная высота:', round(elevation_max), 'м')
    print('Набор:', round(ascent), 'м')
    print('Сброс:', round(descent), 'м')
    print('Высота ночевки:', round(elev), 'м')

if __name__ == '__main__':
    main()