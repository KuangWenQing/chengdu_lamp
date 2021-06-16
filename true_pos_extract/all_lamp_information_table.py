import pandas as pd


def read_lamp_pos_txt():
    ret_dict = {}
    with open("./source_data/lamp_pos.txt", 'r') as fd:
        for row in fd:
            key, val = row.split(':')
            ret_dict['D' + key.strip()] = eval(val)
    return ret_dict


if __name__ == "__main__":
    out_dict = {"id": [], "QR_code": [], "Lamppost": [], "position": []}
    pos_dict = read_lamp_pos_txt()

    df = pd.read_excel("D:/py/chengdu_lamp_position/true_pos_extract/source_data/2021-06-02_董家湾设备信息.xlsx")
    for i in range(len(df)):
        ID = df.loc[i]["ID"]
        QR_code = df.loc[i]["二维码"]
        Lamppost = df.loc[i]["灯杆号"]

        if Lamppost in pos_dict.keys():
            out_dict['id'].append(ID)
            out_dict["QR_code"].append(QR_code)
            out_dict["Lamppost"].append(Lamppost)
            out_dict["position"].append(pos_dict[Lamppost])
    out_df = pd.DataFrame.from_dict(out_dict)

    out_df.to_excel("./lamp_information.xlsx")
