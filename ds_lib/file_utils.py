################################################################################
# Name        : string_utilities
# Description : Includes a few useful functions for making string prettier.
# Version     : 0.0.0
# Created On  : 2022-04-01
# Modified On : 2022-04-01
# Author      : Hamid R. Darabi, Ph.D.
################################################################################

import os
import json
import locale
import string
import numpy as np
import pandas as pd
from glob import glob


class FileUtils:

    @staticmethod
    def read_df(dir, filext="csv"):
        df_list = []
        if filext == "csv":
            for f in glob(os.path.join(dir, "*.csv")):
                df_list.append(pd.read_csv(f))
        if filext == "json":
            for f in glob(os.path.join(dir, "*.json")):
                df_list.append(pd.read_json(f))
        if filext == "parquet":
            for f in glob(os.path.join(dir, "*.parquet")):
                df_list.append(pd.read_parquet(f, engine="fastparquet"))
        else:
            raise ValueError("filetype {} is not in csv, json, parquet".format(filext))
        return pd.concat(df_list)
