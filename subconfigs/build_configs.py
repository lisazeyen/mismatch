import yaml
import numpy as np

with open("../config.yaml", "r") as stream:
    main = yaml.safe_load(stream)

countries = main["scenarios"]["country"]
years = main["scenarios"]["year"]

for c in countries:
    for y in years:

        with open("../config.pypsaeur.yaml", "r") as stream:
            config = yaml.safe_load(stream)

        config["countries"] = [c]
        config["snapshots"]["start"] = f"{y}-01-01"
        config["snapshots"]["end"] = f"{y+1}-01-01"
        config["atlite"]["cutouts"]["europe-2013-era5"]["years"] = [int(y), int(y)]
        era5 = f"europe-{y}-era5"
        config["atlite"]["cutouts"] = {
            era5: config["atlite"]["cutouts"]["europe-2013-era5"]
        }
        for carrier in ["onwind", "offwind-ac", "offwind-dc", "solar", "hydro"]:
            config["renewable"][carrier]["cutout"] = era5

        with open(f"config.pypsaeur{c}{y}.yaml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)
