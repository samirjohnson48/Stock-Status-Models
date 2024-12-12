import os
import pandas as pd
import copernicusmarine
import pickle

area_coords = {
    21: {"lat": [slice(35, 78)], "long": [slice(-80, -42)]},
    27: {
        "lat": [slice(36, 90), slice(43, 90), slice(49, 90)],
        "long": [slice(-42, -6), slice(-6, 0), slice(0, 68)],
    },
    31: {
        "lat": [slice(17, 35), slice(15, 17), slice(8.4, 15), slice(5, 8.4)],
        "long": [slice(-98, -40), slice(-90, -40), slice(-84, -40), slice(-63, -40)],
    },
    34: {"lat": [slice(-6, 36), slice(-6, 8)], "long": [slice(-20, -5), slice(-5, 14)]},
    37: {"lat": [slice(34, 42), slice(30, 47)], "long": [slice(-5, 3), slice(3, 42)]},
    41: {
        "lat": [slice(-60, -34), slice(-50, 5)],
        "long": [slice(-67, -54), slice(-54, -20)],
    },
    47: {"lat": [slice(-40, -6)], "long": [slice(5, 30)]},
    51: {"lat": [slice(-45, 30)], "long": [slice(30, 77)]},
    57: {
        "lat": [slice(-55, 24), slice(-55, -1), slice(-55, -8), slice(-55, -30)],
        "long": [slice(77, 100), slice(100, 105), slice(105, 129), slice(129, 150)],
    },
    61: {
        "lat": [slice(15, 23), slice(20, 65)],
        "long": [slice(105, 115), slice(115, 180)],
    },
    67: {"lat": [slice(40, 66)], "long": [slice(-175, -123)]},
    71: {
        "lat": [slice(-8, 15), slice(15, 20), slice(-25, -8)],
        "long": [slice(99, 129), slice(115, 175), slice(129, 175)],
    },
    77: {
        "lat": [slice(-25, 40), slice(5, 40), slice(5, 15), slice(5, 8)],
        "long": [slice(-175, -120), slice(-120, -98), slice(-98, -84), slice(-84, -78)],
    },
    81: {
        "lat": [slice(-60, -25), slice(-60, -25)],
        "long": [slice(150, 180), slice(-180, -120)],
    },
    87: {
        "lat": [slice(-60, -55), slice(-55, 5)],
        "long": [slice(-120, -67), slice(-120, -69)],
    },
}

years = {
    2004: slice("2004-01-01", "2004-12-31"),
    2006: slice("2006-01-01", "2006-12-31"),
    2008: slice("2008-01-01", "2008-12-31"),
    2009: slice("2009-01-01", "2009-12-31"),
    2011: slice("2011-01-01", "2011-12-31"),
    2013: slice("2013-01-01", "2013-12-31"),
    2015: slice("2015-01-01", "2015-12-31"),
    2017: slice("2017-01-01", "2017-12-31"),
    2019: slice("2019-01-01", "2019-12-31"),
    2021: slice("2021-01-01", "2021-12-31"),
}

dataset1 = copernicusmarine.open_dataset(
    dataset_id="cmems_mod_glo_phy-mnstd_my_0.25deg_P1M-m",
    username=os.getenv("copernicus_username"),
    password=os.getenv("copernicus_password"),
)

dataset2 = copernicusmarine.open_dataset(
    dataset_id="cmems_mod_glo_bgc_my_0.25deg_P1M-m",
    username="sjohnson3",
    password=os.getenv("copernicus_password"),
)

data_template = {year: pd.DataFrame() for year in years.keys()}

oceanography_pickle = "oceanography_data.pkl"
file_path = os.path.dirname(os.getcwd()) + "/model_data/"

oceanography_data = {area: {} for area in area_coords.keys()}

with open(oceanography_pickle, "wb") as file:
    pickle.dump(oceanography_data, file)


def build_data(dataset, pickle_file, variable, depth=0):
    print(f"Loading data for {variable}")

    with open(pickle_file, "rb") as file:
        data = pickle.load(file)

    for key in area_coords.keys():
        data[key][variable] = data_template

    for area, coords in area_coords.items():
        for year, year_slice in years.items():
            temp = pd.DataFrame()
            for lat, long in zip(coords["lat"], coords["long"]):
                if depth is not None:
                    subset = (
                        dataset[[variable]]
                        .isel(depth=depth)
                        .sel(latitude=lat, longitude=long, time=year_slice)
                    )
                else:
                    subset = dataset[[variable]].sel(
                        latitude=lat, longitude=long, time=year_slice
                    )
                temp = pd.concat(
                    [
                        temp,
                        subset[variable].to_dataframe().dropna(),
                    ]
                )

            data[area][variable][year] = (
                temp.groupby("time")[variable].mean().reset_index()
            )
            print(f"Completed year {year} for area {area}")

    with open(pickle_file, "wb") as file:
        pickle.dump(data, file)

    print(f"{variable} data loaded onto {pickle_file}")


build_data(dataset1, oceanography_pickle, "thetao_mean")
build_data(dataset1, oceanography_pickle, "so_mean")
build_data(dataset2, oceanography_pickle, "chl")
build_data(dataset2, oceanography_pickle, "no3")
build_data(dataset2, oceanography_pickle, "po4")
build_data(dataset2, oceanography_pickle, "si")
build_data(dataset2, oceanography_pickle, "nppv")
build_data(dataset2, oceanography_pickle, "o2")
build_data(dataset2, oceanography_pickle, "fe")
build_data(dataset2, oceanography_pickle, "phyc")
build_data(dataset2, oceanography_pickle, "ph")
build_data(dataset2, oceanography_pickle, "spco2", depth=None)
