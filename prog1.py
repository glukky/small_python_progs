import os
import time
# os.rename("/home/turist/Downloads/test_gpx.gpx", "/home/turist/Downloads/test_gpx.txt")
with open('./test_gpx.txt', 'r') as f:

    #ищем строку с trkseg, следующая - начало трека
    point_start = -1
    while point_start == -1:
        str_new = f.readline()
        print(str_new, end='')
        point_start = str_new.find('trkseg')
        print('i=', point_start)

        #вычисляем секунду старта от начала эпохи
        time_pt_start = str_new.find('time')
        if time_pt_start != -1:
            x = str_new[time_pt_start + 5:time_pt_start + 25]
            y = time.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
            sec_start = time.mktime(y)
            print('sec_start=', sec_start)
        print('')

    #собираем данные точек трека
    result_dict = {}
    pt_dict = {}
    i = 0
    break_word = -1
    while break_word == -1:
        str_new = f.readline()
        lat = str_new.find('lat')
        lon = str_new.find('lon')
        ele = str_new.find('ele')
        time_pt = str_new.find('time')
        if lat != -1:
            pt_dict['lat'] = str_new[lat + 5:lat + 15]
            print('lat=', str_new[lat + 5:lat + 15])
            print('Данные точки:', pt_dict)
            lat = -1
        if lon != -1:
            pt_dict['lon'] = str_new[lon + 5:lon +15]
            print('lon=', str_new[lon + 5:lon +15])
            print('Данные точки:', pt_dict)
            lon = -1
        if ele != -1:
            pt_dict['ele'] = str_new[ele + 4:ele + 8]
            print('ele=', str_new[ele + 4:ele + 8])
            print('Данные точки:', pt_dict)
            ele = -1
        if time_pt != -1:
            print('time=', str_new[time_pt + 5:time_pt + 25])
            x = str_new[time_pt + 5:time_pt +25]
            y = time.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
            print(y)
            sec_original = time.mktime(y)
            print('sec_original=', sec_original)
            pt_dict['sec_original'] = sec_original
            print('Данные точки:', pt_dict)
            time_pt = -1

        if len(pt_dict) == 4:
            for key in pt_dict:
                result_dict[i][key] = pt_dict[key]

            i = i + 1
            print(result_dict)
            pt_dict.clear()
        break_word = str_new.find('/trkseg')
# os.rename("/home/turist/Downloads/test_gpx.txt", "/home/turist/Downloads/test_gpx.gpx")
