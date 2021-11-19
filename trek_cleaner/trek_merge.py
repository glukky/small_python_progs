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
        print("Usage: trek_merge.py <input_track1.gpx> ... <input_track_n.gpx> <output_track.gpx>")
        sys.exit(1)

    main_file_name = sys.argv[1]
    output_file_name = sys.argv[-1]

    if os.path.exists(output_file_name):
        print("Sorry, you're trying to destroy your data, please remove it first. Output file must NOT exist.")
        sys.exit(2)

    ns = {'g': _NS}

    print("Loading `{}`...".format(main_file_name))
    main_tree = ET.parse(main_file_name)
    main_root = main_tree.getroot()
    main_trk = main_root.find('g:trk', ns)

    # trkseg_elem - родительские элементы для точек разделённых участков трека
    # т.е. перебираем все ветви <trgseg>...</trkseg>

    for track_index in range(1, len(sys.argv) - 1):
        merged_file_name = sys.argv[track_index]
        print("Merging `{}`...".format(merged_file_name))

        merged_tree = ET.parse(merged_file_name)
        merged_root = merged_tree.getroot()

        for trkseg_elem in merged_root.iterfind('g:trk/g:trkseg', ns):
            main_trk.append(trkseg_elem)

    # Записываем новый xml-документ на основе полученного дерева
    print("Writing `{}`...".format(output_file_name))
    main_tree.write(output_file_name, encoding="UTF-8")
    print("All done")


if __name__ == '__main__':
    main()
