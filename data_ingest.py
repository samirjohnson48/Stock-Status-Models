import pandas as pd
import os

file_path = os.getcwd() + "/data/"

areas = [21, 27, 31, 34, 41, 47, 51, 57, 61, 67, 71, 77]

data_dict = {}

for a in areas:
    area = "area" + str(a)
    data_dict[area] = pd.read_excel(file_path + area + ".xlsx")


