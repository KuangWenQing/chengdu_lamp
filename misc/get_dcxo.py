import os
import pandas as pd

path = r"D:\work\chengdu_fix_analysis\2021-09-07_09_13" + "\\"
df = pd.read_excel(path + "last_gga\\all_lamp_pos_enu.xlsx")

out_df = df.drop(df.columns[[0, 2]], axis=1)        # 删除第 1 、 3 列
col_name = out_df.columns.tolist()
col_name.append('dcxo')     # 增加一列 索引值为 dcxo
out_df = out_df.reindex(columns=col_name)   # 对原列索引重新构建索引值

info_xlsx = [f for f in os.listdir(path) if f.endswith('info.xlsx') and f.startswith('00')]

len_df = len(out_df)
for i in range(len_df):
    for file in info_xlsx:
        if out_df.loc[i]['id'] in file:
            info_df = pd.read_excel(path + file)
            if len(info_df) < 3:
                continue
            dcxo = info_df.loc[1]['sys_cd_dcxo']
            out_df.loc[i, 'dcxo'] = dcxo

out_df.to_excel(path + 'dcxo.xlsx')

