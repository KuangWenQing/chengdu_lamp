import os
from data_analysis.nmea2kml import gga2kml


path = r"C:\Users\wqkuang\Downloads" + "\\"
file_lst = [f for f in os.listdir(path) if f.endswith('.gga')]

for file in file_lst:
    gga2kml(path+file, path+file+'.kml')
