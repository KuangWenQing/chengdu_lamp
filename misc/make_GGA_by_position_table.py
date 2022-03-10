import math
from wgs84_to_gcj02 import gcj02towgs84
import pandas as pd
from base_function import convert_float_to_ll

GGA_Template = "$GPGGA,{},{},N,{},E,1,08,0.9,545.4,M,46.9,M,,*47"

path = r"C:\Users\wqkuang\Downloads" + "\\"


def make_gga(excel_file, is_gcj02=False):
    df = pd.read_excel(path + excel_file)

    fd_pc = open(path + excel_file[:excel_file.index('.')] + "_true.gga", 'w')
    fd_gps = open(path + excel_file[:excel_file.index('.')] + "_gps.gga", 'w')
    minute = 0
    for i in range(len(df)):
        minute += 1
        time_str = "{:0>2d}".format(minute//60) + "{:0>2d}".format(minute % 60) + '00.00'

        lon = df.loc[i]['pc_jd']
        lat = df.loc[i]['pc_wd']
        if lon != lon or lat != lat:
            continue

        if is_gcj02:
            [lon, lat] = gcj02towgs84(lon, lat)
        print(GGA_Template.format(time_str, convert_float_to_ll(lat), convert_float_to_ll(lon)), file=fd_pc)

        lon = df.loc[i]['gps_转换经度']
        lat = df.loc[i]['gps_转换纬度']
        if is_gcj02:
            [lon, lat] = gcj02towgs84(lon, lat)
        print(GGA_Template.format(time_str, convert_float_to_ll(lat), convert_float_to_ll(lon)), file=fd_gps)

    fd_pc.close()
    fd_gps.close()


if __name__ == "__main__":
    make_gga("大误差.xlsx", True)
