import os
# import sys
from base_function import get_llh_from_gga
# sys.path.append("../../")


'''
根据截图时间提取 GGA 语句， 从而得到位置 (经度 纬度 椭球高)
{每盏灯的灯杆号 ： 位置} 保存成文件 lamp_pos.txt
'''


def get_file_create_time(path_):
    lamp_id_dict = {}
    file_lst = [f for f in os.listdir(path_) if f.endswith('.jpg')]
    for file in file_lst:
        id, data_time = file.split("屏幕截图 ")
        hour_min_sec = data_time.split()[1][:-4]
        hour = int(hour_min_sec[:2]) - 8
        if hour < 10:
            h = '0' + str(hour)
        else:
            h = str(hour)
        hms = h + hour_min_sec[2:]
        lamp_id_dict[id] = hms
    return lamp_id_dict


if __name__ == '__main__':
    picture_path = "D:/work/成都路灯位置图/"
    gga_file = "D:/work/0412/COM7_210412_024411.gga"
    lamp_pos = {}
    lamp_id_dict = get_file_create_time(picture_path)
    f_gga = open("./used_gga.txt", 'w')
    f_pos = open("./lamp_pos.txt", 'w')

    with open(gga_file, 'r') as fd:
        for row in fd:
            if "GGA" not in row:
                continue

            for key in lamp_id_dict.keys():
                if lamp_id_dict[key] in row:
                    print(row, file=f_gga)
                    lat, lon, alt_Ell = get_llh_from_gga(row)
                    lamp_pos[key] = (lat, lon, alt_Ell)

    for id in lamp_pos.keys():
        print("%s : %s" % (id, lamp_pos[id]), file=f_pos)
