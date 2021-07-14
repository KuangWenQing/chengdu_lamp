import os, sys
import openpyxl
import numpy as np
import pandas as pd
import shutil
from nmea2kml import gga2kml
from define_struct import parser_str_bin


def write_excel_xlsx(sheet, value, row_cnt=0):
    """ sheet 工作簿
        value 是写的内容
        row_cnt 表示写到表格第几行"""
    index = len(value)
    for i in range(0, index):
        row_cnt += 1
        for j in range(0, len(value[i])):
            sheet.cell(row=row_cnt, column=j+1, value=str(value[i][j]))
    return row_cnt


def excel_row_data(nparr: np.ndarray):
    fall_avepli = nparr['fix_all']['avepli'][0]
    fall_avecnr = nparr['fix_all']['avecnr'][0]
    fall_ircnt = nparr['fix_all']['ircnt'][0]
    fall_nval = nparr['fix_all']['nval'][0]
    warn_pv_rate_0 = nparr['fix_all']['warn_pv_rate'][0][0]
    warn_pv_rate_1 = nparr['fix_all']['warn_pv_rate'][0][1]
    fall_avensv = nparr['fix_all']['avensv'][0]

    fstat_nsv = nparr['fstat']['nsv'][0]
    fstat_sv = nparr['fstat']['sv'][0]
    fstat_avepli = nparr['fstat']['avepli'][0]
    fstat_avecnr = nparr['fstat']['avecnr'][0]
    fstat_svnfix = nparr['fstat']['svnfix'][0]
    fstat_rw_flag = nparr['fstat']['rw_flag'][0]
    fstat_ircnt = nparr['fstat']['ircnt'][0]
    fstat_nval = nparr['fstat']['nval'][0]
    fstat_avensv = nparr['fstat']['avensv'][0]

    sys_cd_dcxo = nparr['sys']['dcxo'][0]
    sys_cd_nval = nparr['sys']['nval'][0]
    sys_cd_ircnt = nparr['sys']['ircnt'][0]
    sys_cd_rstcnt = nparr['sys']['rstcnt'][0]
    sys_cd_rsttype = nparr['sys']['rsttype'][0]

    trk_cd_nval = nparr['trk']['nval'][0]
    trk_cd_nsv = nparr['trk']['nsv'][0]
    trk_cd_sv = nparr['trk']['sv'][0]
    trk_cd_avepli = nparr['trk']['avepli'][0]
    trk_cd_avecnr = nparr['trk']['avecnr'][0]
    trk_cd_trk = nparr['trk']['svntrk'][0]
    trk_cd_avensv = nparr['trk']['avensv'][0]

    write_row_data = [fall_avepli, fall_avecnr, fall_avensv, fall_ircnt, fall_nval, warn_pv_rate_0, warn_pv_rate_1,
                      fstat_nsv, fstat_rw_flag, fstat_ircnt, fstat_nval, fstat_avensv, fstat_sv, fstat_avepli,
                      fstat_avecnr, fstat_svnfix, sys_cd_dcxo, sys_cd_nval, sys_cd_ircnt, sys_cd_rstcnt, sys_cd_rsttype,
                      trk_cd_nval, trk_cd_nsv, trk_cd_sv, trk_cd_avepli, trk_cd_avecnr, trk_cd_trk, trk_cd_avensv]
    return write_row_data


def excel_write(write_value):
    head_xlsx = [["time", "fall_avepli", "fall_avecnr", "fall_avensv", "fall_ircnt", "fall_nval", "warn_pv_rate_0",
                  "warn_pv_rate_1", "fstat_nsv", "fstat_rw_flag", "fstat_ircnt", "fstat_nval", "fstat_avensv",
                  "fstat_sv", "fstat_avepli", "fstat_avecnr", "fstat_svnfix", 'sys_cd_dcxo', 'sys_cd_nval',
                  'sys_cd_ircnt', 'sys_cd_rstcnt', 'sys_cd_rsttype', 'trk_cd_nval', 'trk_cd_nsv', 'trk_cd_sv',
                  'trk_cd_avepli', 'trk_cd_avecnr', 'trk_cd_trk', 'trk_cd_avesv', "picture", "kml"], [file]]
    book_name_xlsx = path + file_name + '_info.xlsx'

    wb = openpyxl.Workbook()  # 创建一个workbook对象，而且会在workbook中至少创建一个表worksheet
    ws = wb.active  # 获取当前活跃的worksheet,默认就是第一个worksheet
    row_xlsx = write_excel_xlsx(ws, head_xlsx, row_cnt=0)

    row_renew = write_excel_xlsx(ws, write_value, row_xlsx)
    wb.save(book_name_xlsx)
    wb.close()
    return row_renew


def gga_produce(nparr: np.ndarray, gga_time="080808.00"):
    gga_Template = "$GPGGA,%s,%s,N,%s,E,1,10,1.22,%.3f,M,-8.00,M,,*78"

    lon = (float(nparr['plla']['lon']['fDat']) + float(nparr['plla']['lon']['fErr'])) * 180.0 / 3.1415926
    lat = (float(nparr['plla']['lat']['fDat']) + float(nparr['plla']['lat']['fErr'])) * 180.0 / 3.1415926

    minute = np.fabs(round(float(lon - int(lon)) * 60, 4))
    if minute < 10:
        lon_str = str(int(lon)) + '0' + str(minute)
    else:
        lon_str = str(int(lon)) + str(minute)

    minute = np.fabs(round(float(lat - int(lat)) * 60, 4))
    if minute < 10:
        lat_str = str(int(lat)) + '0' + str(minute)
    else:
        lat_str = str(int(lat)) + str(minute)

    alt = float(nparr['plla']['alt'])
    return gga_Template % (gga_time, lat_str, lon_str, alt)


light_ID = ('000b7e42321d', '000b7e423210', '000b7e4231d6', '000b7e4231c9', '000b7e42317c',
            '000b7e423136', '000b7e42320f', '000b7e4231d3', '000b7e4232f9', '000b7e4231c4')
light_pole_number = ('D1', 'D11', 'D21', 'D31', 'D51', 'D61', 'D71', 'D81', 'D91', 'D101')

light_dict = dict(zip(light_ID, light_pole_number))
print(light_dict)


path = "D:\\work\\chengdu_log\\tmp\\"
file_lst = (f for f in os.listdir(path) if f.endswith('.csv'))


if __name__ == "__main__":
    date_list = []
    for file in file_lst:
        file_name = file[:-4]
        if file_name not in light_ID:
            continue
        time_of_date_bak = ""
        write_data = []
        gga = ''
        gga_bak = ''
        hour_bak = -1
        gga_path_name_last = path + file_name + '_last.gga'
        fd_whole_gga = open(path + file_name + "_whole.gga", 'w')
        fd_gga_last = open(gga_path_name_last, 'w')
        fd_gga = None
        print(file)

        sheet_data = pd.read_csv(path + file)
        time_lst = sheet_data.iloc[:, 0]

        bin_data = sheet_data['hexContent']
        len_list = len(time_lst)
        for i in range(len_list):
            time = time_lst[i]
            str_bin = ''
            try:
                str_bin = bin_data[i].split('47 50 53 3A ')[1]
            except AttributeError:
                print(time, " bin data is abnormal")
                continue
            time_of_date, time_of_hms = time.split('T')
            if not fd_gga:
                gga_path_name = path + file_name + "_" + time_of_date + '.gga'
                fd_gga = open(gga_path_name, 'w')

                isExists = os.path.exists(path + time_of_date)
                if not isExists:
                    os.mkdir(path + time_of_date)
                date_list.append(time_of_date)

            time_of_hms = time_of_hms[: -1]
            hour_str, min_str, sec_str = time_of_hms.split(":")
            gga_time = hour_str + min_str + sec_str

            ret_arr = parser_str_bin(str_bin)
            if not ret_arr:
                continue
            gga = gga_produce(ret_arr, gga_time)
            print(gga, file=fd_whole_gga)

            hour_now = int(hour_str)
            if hour_bak != -1:
                if 2 < np.fabs(hour_bak - hour_now) < 20:
                    fd_gga.close()
                    gga_path_name = path + file_name + "_" + time_of_date + '.gga'
                    fd_gga = open(gga_path_name, 'w')
                    isExists = os.path.exists(path + time_of_date)
                    if not isExists:
                        os.mkdir(path + time_of_date)
                    date_list.append(time_of_date)
                    print(gga, file=fd_gga_last)
                print(gga, file=fd_gga)
            else:
                print(gga, file=fd_gga_last)
                print(gga, file=fd_gga)
            hour_bak = hour_now
            gga_bak = gga

            write_data.append([time] + excel_row_data(ret_arr))
        excel_write(write_data)
        fd_gga.close()
        fd_gga_last.close()
        fd_whole_gga.close()

    gga_file_lst = (f for f in os.listdir(path) if f.endswith('.gga'))
    for file in gga_file_lst:
        gga_path_name = path + file
        if os.path.getsize(gga_path_name):
            kml_path_name = gga_path_name[:-3] + "kml"
            # os.system('pythonw3 ./nmea2kml.py ' + gga_path_name + '>' + kml_path_name)
            gga2kml(gga_path_name, kml_path_name)
        else:
            os.remove(gga_path_name)

    date_file = (f for f in os.listdir(path) if 'whole' not in f and 'last' not in f)
    for file in date_file:
        path_file = path + file
        if os.path.isdir(path_file):     # 是子文件夹
            continue
        for date in date_list:
            if date in file:
                shutil.move(path_file, path+date+'/'+file)
                break

    os.mkdir(path + 'last_gga')
    last_file = (f for f in os.listdir(path) if 'last' in f)
    for file in last_file:
        shutil.move(path + file, path + 'last_gga')

    os.mkdir(path + 'whole_gga')
    whole_file = (f for f in os.listdir(path) if 'whole' in f)
    for file in whole_file:
        shutil.move(path + file, path + 'whole_gga')
