import struct
import collections
from collections import namedtuple
import numpy as np


bin_str = "00 00 00 00 00 00 00 00 00 00 00 00 DB 0F C9 BF 2E BD 3B 33 21 FE C1 CA 00 00 00 00 41 06 00 00 00 00 00 00 " \
          "34 FF C4 3E F0 A6 EC 3E 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 41 06 00 00 00 00 00 00 34 FF C4 3E " \
          "F0 A6 EC 3E 00 00 00 00 0D 02 00 00 00 00 00 00 41 06 00 00 02 00 00 00 08 00 00 00 41 06 00 00 00 00 00 00 " \
          "0C 0E 04 13 01 00 00 00 00 00 00 00 07 04 07 0C 0B 00 00 00 00 00 00 00 25 2A 25 1F 1E 00 00 00 00 00 00 00 " \
          "25 05 00 00 25 05 00 00 25 05 00 00 CD 02 00 00 CB 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 " \
          "00 00 00 00 7E 2F 57 40 BC 0F 77 EE "


TYP_F32 = np.dtype([('fDat', np.float32), ('fErr', np.float32)], align=True)                # 扩展float
STU_COOR_LLA = np.dtype([('lon', TYP_F32), ('lat', TYP_F32), ('alt', 'f4')], align=True)    # 经 纬 高
fix_all_t = np.dtype([('avepli', 'u1'), ('avecnr', 'u1'),           # 用于定位星的平均pli  平均载噪比
                      ('ircnt', 'u4'), ('nval', 'u4'),              # 累计中断数    累计有效定位数
                      ('warn_pv_rate', 'f4', 2), ('avensv', 'f4')], align=True)

fstat_t = np.dtype([('nsv', 'u4'), ('sv', 'u1', 12),
                    ('avepli', 'u1', 12), ('avecnr', 'u1', 12),
                    ('svnfix', 'u4', 10), ('rw_flag', 'u4'),
                    ('ircnt', 'u4'), ('nval', 'u4'),
                    ('warn_pv_rate', 'f4', 2), ('avensv', 'f4')], align=True)

sys_cd_t = np.dtype([('dcxo', 'i4'), ('nval', 'u4'), ('ircnt', 'u4'),
                     ('rstcnt', 'u4'), ('rsttype', 'u4')], align=True)

trk_cd_t = np.dtype([('nval', 'u4'), ('nsv', 'u4'), ('sv', 'u1', 12),
                     ('avepli', 'u1', 12), ('avecnr', 'u1', 12),
                     ('svntrk', 'u4', 10), ('avensv', 'f4')], align=True)

fsol_cd_t = np.dtype([('lst', 'u2'), ('lpsys', 'u1'), ('val', 'u1'),
                      ('plla', STU_COOR_LLA), ('fix_all', fix_all_t),
                      ('fstat', fstat_t), ('sys', sys_cd_t), ('trk', trk_cd_t)], align=True)

# Typ_f32 = namedtuple('Typ_f32', ['fDat', 'fErr'])
# Stu_coor_lla = namedtuple('Stu_coor_lla', ['lon', 'lat', 'alt'])
# Fix_all_t = namedtuple('Fix_all_t', ['avepli', 'avecnr', 'ircnt', 'nval', 'warn_pv_rate', 'avesv'])
# Fstat_t = namedtuple('Fstat_t', ['nsv', 'sv', 'avepli', 'avecnr', 'svnfix', 'rw_flag', 'ircnt', 'nval', 'warn_pv_rate', 'avensv'])
# Sys_cd_t = namedtuple('Sys_cd_t', ['dcxo', 'nval', 'sv', 'rstcnt', 'rsttype'])
# Trk_cd_t = namedtuple('Trk_cd_t', ['nval', 'nsv', 'sv', 'avepli', 'avecnr', 'svntrk', 'avensv'])
# Fsol_cd_t = namedtuple('Fsol_cd_t', ['lst', 'lpsys', 'val', 'plla', 'fix_all', 'fstat', 'sys', 'trk'])


def str_bin_to_arr(ss: str):
    return [int(s, 16) for s in ss.split()]


def parser_str_bin(ss: str):
    need_bytes = fsol_cd_t.itemsize
    input_byte_data = str_bin_to_arr(ss)

    if len(input_byte_data) < need_bytes:
        print("input data len  %d < %d need_data len" % (len(input_byte_data), need_bytes))
        return None
    mm = struct.pack('B'*need_bytes, *input_byte_data[:need_bytes])
    return np.frombuffer(mm, dtype=fsol_cd_t)


if __name__ == "__main__":
    ret = parser_str_bin(bin_str)
    print('!')
