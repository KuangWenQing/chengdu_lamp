import os
import numpy as np
import pandas as pd

from base_function import ecef_to_enu, lla_to_xyz, xyz_to_lla

path = r"D:\work\chengdu_log_analysis\2021-08-30_08_31 device log" + "\\"
# path = "d:/work/temp/"
folder_lst = [item for item in os.listdir(path) if os.path.isdir(path + item) and '-' in item]
df = pd.read_excel("../true_pos_extract/lamp_information.xlsx")
out_en_df = df.copy()
del out_en_df['position']
del out_en_df["Unnamed: 0"]
out_enu_df = out_en_df.copy()


def get_true_pos(file_name: str):
    lamp_id = file_name.split('.')[0]
    for i in range(len(df)):
        if df.loc[i]["id"] == lamp_id:
            return df.loc[i]["position"]
    return None


def get_last_r_ave(pathname: str):
    ret = ''
    with open(pathname, 'r') as fp:
        for line in fp:
            if line.startswith("DEBUG R AVE, tot"):
                ret = line
    if ret:
        return ret
    else:
        return False


def analysis_folder(folder_):
    file_lst = [f for f in os.listdir(path + '/' + folder_) if f.endswith('log')]
    for name in file_lst:
        true_pos = get_true_pos(name)
        if not true_pos:
            print("we haven't this lamp: %s" % name)
            continue
        path_name = path + '/' + folder_ + '/' + name
        print(path_name)
        r_ave = get_last_r_ave(path_name)
        if not r_ave:
            print("this file no 'R AVE' \\n")
            continue

        lamp_id = name.split('.')[0]
        loc_num = out_en_df.loc[df['id'] == lamp_id].index[0]
        en, enu = analysis_r_ave(r_ave, true_pos)
        out_en_df.loc[loc_num][folder_[folder_.index('-') + 1:]] = en
        out_enu_df.loc[loc_num][folder_[folder_.index('-')+1:]] = enu


def parsing_r_ave_to_lla(r_ave: str):
    ret = r_ave.split(',')
    x = float(ret[3])
    y = float(ret[4])
    z = float(ret[5])
    return x, y, z


def analysis_r_ave(r_ave, true_pos):
    true_pos_lla = eval(true_pos)
    true_xyz = lla_to_xyz(*true_pos_lla)
    xyz = parsing_r_ave_to_lla(r_ave)
    dis_xyz = np.linalg.norm(np.array(true_xyz) - np.array(xyz))

    lla = xyz_to_lla(*xyz)
    enu = ecef_to_enu(true_xyz[0], true_xyz[1], true_xyz[2], lla[0], lla[1], lla[2])
    dis_en = np.linalg.norm(enu[:2])
    return round(dis_en, 2), round(dis_xyz, 2)


if __name__ == "__main__":
    for folder in folder_lst:
        out_en_df[folder[folder.index('-')+1:]] = [None for i in range(len(out_en_df))]
        out_enu_df[folder[folder.index('-') + 1:]] = [None for i in range(len(out_enu_df))]
        analysis_folder(folder)
    out_en_df.to_excel(path + '\\all_lamp_pos_en.xlsx')
    out_enu_df.to_excel(path + '\\all_lamp_pos_enu.xlsx')








