
import multiprocessing as mp
import os

import pandas as pd

from config import (
    PREPROCESSED_HOMES_DATASETS_DIR,
    PREPROCESSED_DATASET_FILENAME_SUFFIX,
    SRC_HOMES_DATASETS_DIR,
    START_DATE,
    END_DATE
)

from utils.preprocessing import prepare_data


# noinspection PyShadowingNames
def prepare_homes_data(
        src_homes_folder,
        preprocessed_homes_datasets_path,
        min_date,
        max_date,
        disabled_t_threshold
):
    ntc = 1
    processes = []
    for dataset_name in os.listdir(src_homes_folder):
        file_path = "{}\\{}".format(src_homes_folder, dataset_name)
        process = mp.Process(
            target=prepare_one_home_data,
            args=(
                preprocessed_homes_datasets_path,
                dataset_name,
                file_path,
                (min_date, max_date, disabled_t_threshold), {"ntc": ntc})
        )
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


def prepare_one_home_data(target_datasets_dir, dataset_name, src_file_path, args, kwargs):
    print("Processing dataset {}".format(src_file_path))
    df = pd.read_csv(src_file_path, sep=';', low_memory=False)
    df = prepare_data(df, *args, **kwargs)

    dst_filename = f"{target_datasets_dir}\\{dataset_name}{PREPROCESSED_DATASET_FILENAME_SUFFIX}"
    print("Saving to {}".format(dst_filename))
    df.to_pickle(dst_filename)


if __name__ == '__main__':
    disabled_t_threshold = 0  # 35

    prepare_homes_data(
        SRC_HOMES_DATASETS_DIR,
        PREPROCESSED_HOMES_DATASETS_DIR,
        START_DATE,
        END_DATE,
        disabled_t_threshold
    )
