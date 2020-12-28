
import pandas as pd

from config import (
    SRC_BOILER_DATASET_PATH,
    PREPROCESSED_BOILER_DATASET_PATH,
    START_DATE,
    END_DATE
)
from utils.preprocess_utils import prepare_data


# noinspection PyShadowingNames
def prepare_boilers_data(
        src_boiler_dataset_path,
        preprocessed_boiler_dataset_path,
        min_date,
        max_date,
        disabled_t_threshold
):
    print("Loading {}".format(src_boiler_dataset_path))
    boilers_df = pd.read_csv(src_boiler_dataset_path, sep=";", low_memory=False)

    print("Processing data")
    preprocessed_boiler_df = prepare_data(boilers_df, min_date, max_date, disabled_t_threshold)

    print("Saving to {}".format(preprocessed_boiler_dataset_path))
    preprocessed_boiler_df.to_pickle(preprocessed_boiler_dataset_path)


if __name__ == '__main__':
    disabled_t_threshold = 0  # 35

    prepare_boilers_data(
        SRC_BOILER_DATASET_PATH,
        PREPROCESSED_BOILER_DATASET_PATH,
        START_DATE,
        END_DATE,
        disabled_t_threshold
    )
