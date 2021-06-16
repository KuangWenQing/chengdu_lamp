import os
import sys

import matplotlib.pyplot as plt
import pandas as pd

from base_function import analysis_gga, lla_to_xyz, sort_and_print_50_95_99

path = "D:\\work\\chengdu_log\\2021-06-01_06_15\\"
file_lst = [f for f in os.listdir(path) if f.endswith('whole.gga')]
df = pd.read_excel("../true_pos_extract/lamp_information.xlsx")


def get_true_pos(file_name: str):
    lamp_id = file_name.split('_')[0]
    for i in range(len(df)):
        if df.loc[i]["id"] == lamp_id:
            return df.loc[i]["position"]
    return None


def analysis_file(pathname: str, true_xyz_: tuple):
    dis_xyz_lst = []
    dis_en_lst = []
    with open(pathname, 'r') as fd:
        for row in fd:
            time_sec, llh, xyz, ENU, dis_xyz, dis_en = analysis_gga(true_xyz_, row)
            dis_xyz_lst.append(round(dis_xyz, 2))
            dis_en_lst.append(round(dis_en, 2))
    return dis_xyz_lst, dis_en_lst


if __name__ == "__main__":

    for name in file_lst:
        print(name)
        true_pos = get_true_pos(name)
        if not true_pos:
            print("we haven't this lamp")
            sys.exit()
        print("lla = ", true_pos)
        true_pos_lla = eval(true_pos)
        true_xyz = lla_to_xyz(*true_pos_lla)
        print("xyz = ", true_xyz)
        xyz_diff, en_diff = analysis_file(path + name, true_xyz)
        print("ENU", xyz_diff)
        sort_and_print_50_95_99(xyz_diff, 'ENU')
        print("EN", en_diff)
        sort_and_print_50_95_99(en_diff, 'EN')
        print()

        fig1 = plt.figure(1)
        plt.suptitle(name)
        plt.subplot(211)
        plt.title('ENU')
        plt.plot([x for x in range(len(xyz_diff))], xyz_diff, marker='*', label='enu')
        plt.subplot(212)
        plt.title('EN')
        plt.plot([x for x in range(len(en_diff))], en_diff, marker='x', label='nu')
        plt.legend()  # 不加该语句无法显示 label
        plt.draw()
        plt.savefig(path + name + '.jpg')
        plt.pause(5)  # 显示秒数
        plt.close(fig1)





