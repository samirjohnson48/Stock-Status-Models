import pandas as pd
import numpy as np
import os

# Ingest data for 2021 new method by area and country

file_path = os.path.dirname(os.getcwd()) + "/data/"

areas = [21, 27, 31, 34, 41, 47, 51, 57, 61, 67, 71, 77]

country_dict = {}
area_dict = {}

for a in areas:
    area = "area" + str(a)
    if a == 47:
        country_dict[area + "_2021"] = pd.read_excel(file_path + area + ".xlsx", skiprows=3)
    else:
        country_dict[area + "_2021"] = pd.read_excel(file_path + area + ".xlsx")
    area += "_2021"
    if any(
        col in country_dict[area].columns
        for col in [
            "Status (3 levels)",
            "M",
            "Location (Country? geographic region?)",
        ]
    ):
        country_dict[area] = country_dict[area].rename(
            columns={
                "Location (Country? geographic region?)": "Location",
                "Status (3 levels)": "Status",
                "M": "Status",
            }
        )
    if "Country" not in country_dict[area].columns:
        country_dict[area]["Country"] = np.nan
    elif "Location" not in country_dict[area].columns:
        country_dict[area]["Location"] = np.nan
    country_dict[area] = country_dict[area][["Location", "Status", "Country"]]
    country_dict[area]["Status"] = country_dict[area]["Status"].replace(
        {"?": np.nan, "F": "M"}
    )

    area_dict[area] = pd.DataFrame(
        {
            "Area": [area] * len(country_dict[area]),
            "Status": country_dict[area]["Status"],
        }
    )

    country_dict[area]["Country"] = country_dict[area]["Country"].fillna(
        country_dict[area]["Location"]
    )

    country_dict[area].drop(columns=["Location"], inplace=True)

    country_dict[area] = country_dict[area].dropna()

    country_dict[area]["Status"] = country_dict[area]["Status"].str[0].str.upper()
    area_dict[area]["Status"] = area_dict[area]["Status"].str[0].str.upper()

area_dict["area61_2021"]["Status"] = area_dict["area61_2021"]["Status"].replace("F", "M")


combined_country = pd.concat(country_dict.values(), ignore_index=True, axis=0)
combined_area = pd.concat(area_dict.values(), ignore_index=True, axis=0)

status_ratios_2021 = (
    combined_area.groupby(["Area", "Status"])
    .size()
    .div(combined_area.groupby("Area").size(), level="Area")
    .unstack(fill_value=0)
)

status_ratios_2021 = status_ratios_2021.reset_index()

status_ratios_2021["S"] = 1 - status_ratios_2021[["O"]]
status_ratios_2021 = status_ratios_2021[["Area", "S"]]

# Ingest data with old method

file_name = "old_method_data.xlsx"

data_old_method = pd.read_excel(file_path + file_name)

area_mapping = {
    "FAO Major Fishing Area: Pacific, Eastern Central": 77,
    "FAO Major Fishing Area: Pacific, Northeast": 67,
    "FAO Major Fishing Area: Pacific, Northwest": 61,
    "FAO Major Fishing Area: Pacific, Western Central": 71,
    "FAO Major Fishing Area: Pacific, Southwest": 81,
    "FAO Major Fishing Area: Pacific, Southeast": 87,
    "FAO Major Fishing Area: Atlantic, Northwest": 21,
    "FAO Major Fishing Area: Atlantic, Northeast": 27,
    "FAO Major Fishing Area: Indian Ocean, Eastern": 57,
    "FAO Major Fishing Area: Indian Ocean, Western": 51,
    "FAO Major Fishing Area: Atlantic, Southeast": 47,
    "FAO Major Fishing Area: Atlantic, Western Central": 31,
    "FAO Major Fishing Area: Atlantic, Eastern Central": 34,
    "FAO Major Fishing Area: Atlantic, Southwest": 41,
    "FAO Major Fishing Area: Mediterranean and Black Sea": 37
}

data_old_method["Area"] = data_old_method["Area"].replace(area_mapping)

data_old_method = data_old_method.sort_values(by=['Area', 'Year'], ascending=[True, True])

print(data_old_method)

