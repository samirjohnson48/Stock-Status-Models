import pandas as pd
import os
import pickle

file_path = os.path.dirname(os.getcwd()) + "/raw_data/"

# Load in FAO Area to Country map

conversion_path = os.path.dirname(os.getcwd()) + "/conversions/"

with open(conversion_path + "area_to_country.pkl", "rb") as file:
    area_to_country = pickle.load(file)

# Load in mapping from FAO countries to WEO (World Economic Outlook) countries
    
with open(conversion_path + "countries_mapping_rev.pkl", "rb") as file:
    countries_mapping_rev = pickle.load(file)

# Convert area to country map to WEO countries naming
    
def map_countries(country_list):
    return [countries_mapping_rev[country] for country in country_list if country in countries_mapping_rev]

area_to_country["Countries"] = area_to_country["Countries"].apply(map_countries)

# Function for aggregating economic data
# Saves data in dictionary with keys as FAO area
# and values as timeseries DataFrame from 2004-2021

def aggregate_econ_data(
    data,
    cols=[
        "2004",
        "2005",
        "2006",
        "2007",
        "2008",
        "2009",
        "2010",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
    ],
    area_to_country=area_to_country
):
    area_econ = {}

    for area, countries in zip(area_to_country["Area"], area_to_country["Countries"]):
        area_econ[area] = pd.DataFrame([[0] * len(cols)], columns=cols)
        count = 0
        for c in countries:
            temp = data[data["COUNTRY.Name"] == c].reset_index()[cols]
            if not (temp.isna().any().any() or len(temp) == 0):
                area_econ[area] += temp
                count += 1
        area_econ[area] /= count
        area_econ[area] = area_econ[area].iloc[0].to_dict()

    return area_econ 

# Load in the economic data

cpi_fab = pd.read_csv(file_path + "cpi_food_and_beverage.csv")
gdp_pc = pd.read_csv(file_path + "gdp_per_capita.csv")
unemp = pd.read_csv(file_path + "unemployment_rate.csv")
pop = pd.read_csv(file_path + "population.csv")
imp_pc = pd.read_csv(file_path + "imports_percent_change.csv")
ex_pc = pd.read_csv(file_path + "exports_percent_change.csv")

# Aggregate data by area

cpi_fab_area = aggregate_econ_data(cpi_fab)
gdp_pc_area = aggregate_econ_data(gdp_pc)
unemp_area = aggregate_econ_data(unemp)
pop_area = aggregate_econ_data(pop)
imp_pc_area = aggregate_econ_data(imp_pc)
ex_pc_area = aggregate_econ_data(ex_pc)

# Pickle data into model_data folder

model_data_path = os.path.dirname(os.getcwd()) + "/model_data/"

def save_econ_data(data, file_name):
    with open(model_data_path + file_name, "wb") as file:
        pickle.dump(data, file)
    
    print(f"Successfully saved {file_name} to {model_data_path}")

save_econ_data(cpi_fab_area, "cpi_fab.pkl")
save_econ_data(gdp_pc_area, "gdp_pc.pkl")
save_econ_data(unemp_area, "unemp.pkl")
save_econ_data(pop_area, "pop.pkl")
save_econ_data(imp_pc_area, "imp_pc.pkl")
save_econ_data(ex_pc_area, "ex_pc.pkl")