import time

# скрипт подставляет новое время в точки трека
# трек стравы, на выходе фрагмент внутри trkseg

with open('/home/turist/Downloads/Zaminka4711578993_3.gpx', 'r') as f:

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
            print('Секунды от начала трека:', sec_original - sec_start)
            pt_dict['sec_original'] = sec_original - sec_start
            print('Данные точки:', pt_dict)
            time_pt = -1
        if len(pt_dict) == 4:
            result_dict[i] = {}
            for key in pt_dict:
                result_dict[i][key] = pt_dict[key]
            i = i + 1
            print(result_dict)
            pt_dict.clear()
        break_word = str_new.find('/trkseg')

#Вычисляем поправочный коэффициент времени k для нового трека

#Время старта нового трека от начала эпохи
str_new = '    <time>2021-01-31T12:46:22Z</time>'
time_pt_start = str_new.find('time')
x = str_new[time_pt_start + 5:time_pt_start + 25]
y = time.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
sec_start = time.mktime(y)
print('Время старта нового трека от начала эпохи:', sec_start)

#Время финиша нового трека от начала эпохи
str_new = '    <time>2021-01-31T13:21:14Z</time>'
time_pt_start = str_new.find('time')
x = str_new[time_pt_start + 5:time_pt_start + 25]
y = time.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
sec_finish = time.mktime(y)
print('Время финиша нового трека от начала эпохи:', sec_finish)
print(sec_finish - sec_start)
k = (sec_finish - sec_start) / result_dict[i - 1]['sec_original']
print('k=', k)

#Формируем новый файл точек трека с учетом коэффициента k
with open('/home/turist/Downloads/test_gpx_new.gpx', 'w') as f:
    for key in result_dict:
        lat = result_dict[key]['lat']
        lon = result_dict[key]['lon']
        str_new = '   <trkpt lat="' + lat + '" lon="' + lon + '">' + '\n'
        #print(str_new)
        f.write(str_new)
        ele = result_dict[key]['ele']
        str_new = '    <ele>' + ele + '</ele>' + '\n'
        #print(str_new)
        f.write(str_new)
        sec_new = int(result_dict[key]['sec_original'] * k + sec_start)
        sec_new_st = time.localtime(sec_new)
        #print(sec_new_st)
        str_new = time.strftime('    <time>%Y-%m-%dT%H:%M:%SZ</time>', sec_new_st) +'\n'
        #print(str_new)
        f.write(str_new)
        str_new = '   </trkpt>' + '\n'
        f.write(str_new)
