import pandas as pd
import os
import matplotlib.pyplot as plt

file_path = os.path.dirname(os.getcwd()) + "/raw_data/"

effort_data = pd.read_excel(file_path + "FAOEffortBOB.xlsx", sheet_name="MappedFAO")
capture_data = pd.read_csv(file_path + "Capture_quantity.csv")
country_codes = pd.read_csv(file_path + "Country_codes.csv")

un_to_iso3 = dict(zip(country_codes["UN"], country_codes["ISO3"]))
capture_data["COUNTRY.UN_CODE"] = capture_data["COUNTRY.UN_CODE"].map(un_to_iso3)
capture_data.rename(columns={"COUNTRY.UN_CODE": "ISO3", "PERIOD": "Year"}, inplace=True)

effort_data = (
    effort_data.groupby(["Year", "ISO3"])[
        [
            "EffortCellReportedNom",
            "EffortCellReportedEff",
            "EffortCellIUUNom",
            "EffortCellIUUEff",
        ]
    ]
    .sum()
    .reset_index()
)

CE_data = pd.merge(
    capture_data,
    effort_data,
    on=["ISO3", "Year"],
    how="inner",
)

CE_data = CE_data.dropna()
CE_data["CPUE"] = CE_data["VALUE"] / CE_data["EffortCellReportedEff"]

print(CE_data[CE_data["SPECIES.ALPHA_3_CODE"] == "FCP"])

