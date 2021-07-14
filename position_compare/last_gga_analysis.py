import os
import sys

import pandas as pd

from base_function import analysis_gga, lla_to_xyz, sort_and_print_50_95_99

path = "D:\\work\\chengdu_log\\2021-07-4_07_11\\"
path += 'last_gga\\'
folder_lst = [item for item in os.listdir(path) if os.path.isdir(path + item)]
df = pd.read_excel("../true_pos_extract/lamp_information.xlsx")
out_en_df = df.copy()
del out_en_df['position']
del out_en_df["Unnamed: 0"]
out_enu_df = out_en_df.copy()


def get_true_pos(file_name: str):
    lamp_id = file_name.split('_')[0]
    for i in range(len(df)):
        if df.loc[i]["id"] == lamp_id:
            return df.loc[i]["position"]
    return None


def analysis_folder(folder_):
    file_lst = [f for f in os.listdir(path + '/' + folder_) if f.endswith('.gga')]
    for name in file_lst:
        true_pos = get_true_pos(name)
        if not true_pos:
            print("we haven't this lamp: %s" % name)
            continue
        path_name = path + '/' + folder_ + '/' + name
        print(path_name)
        lamp_id = name.split('_')[0]
        loc_num = out_en_df.loc[df['id'] == lamp_id].index[0]
        en, enu = analysis_last_gga_file(path_name, true_pos)
        out_en_df.loc[loc_num][folder_[folder_.index('-') + 1:]] = en
        out_enu_df.loc[loc_num][folder_[folder_.index('-')+1:]] = enu


def analysis_last_gga_file(path_name, true_pos):
    true_pos_lla = eval(true_pos)
    true_xyz = lla_to_xyz(*true_pos_lla)

    fd = open(path_name, 'r')
    time_sec, llh, xyz, ENU, dis_xyz, dis_en = analysis_gga(true_xyz, fd.readline())
    fd.close()
    return round(dis_en, 2), round(dis_xyz, 2)


if __name__ == "__main__":
    for folder in folder_lst:
        out_en_df[folder[folder.index('-')+1:]] = [None for i in range(len(out_en_df))]
        out_enu_df[folder[folder.index('-') + 1:]] = [None for i in range(len(out_enu_df))]
        analysis_folder(folder)
    out_en_df.to_excel(path + 'all_lamp_pos_en.xlsx')
    out_enu_df.to_excel(path + 'all_lamp_pos_enu.xlsx')








