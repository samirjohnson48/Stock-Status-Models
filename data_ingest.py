import pandas as pd
import numpy as np
import os

file_path = os.getcwd() + "/data/"

areas = [21, 27, 31, 34, 41, 47, 51, 57, 61, 67, 71, 77]

data_dict = {}

for a in areas:
    area = "area" + str(a)
    if a == 47:
        data_dict[area] = pd.read_excel(file_path + area + ".xlsx", skiprows=3)
    else:
        data_dict[area] = pd.read_excel(file_path + area + ".xlsx")
    if any(
        col in data_dict[area].columns
        for col in [
            "Status (3 levels)",
            "M",
            "Location (Country? geographic region?)",
        ]
    ):
        data_dict[area] = data_dict[area].rename(
            columns={
                "Location (Country? geographic region?)": "Location",
                "Status (3 levels)": "Status",
                "M": "Status",
            }
        )
    if "Country" not in data_dict[area].columns:
        data_dict[area]["Country"] = np.nan
    elif "Location" not in data_dict[area].columns:
        data_dict[area]["Location"] = np.nan
    data_dict[area] = data_dict[area][["Location", "Status", "Country"]]

    data_dict[area]["Location"] = data_dict[area]["Country"].fillna(
        data_dict[area]["Location"]
    )

    data_dict[area].drop(columns=["Country"], inplace=True)

    data_dict[area] = data_dict[area].dropna()

    data_dict[area]["Status"] = data_dict[area]["Status"].str[0].str.upper()


combined_df = pd.concat(data_dict.values(), ignore_index=True, axis=0)

print(combined_df)
