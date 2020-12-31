import logging
import os
import multiprocessing as mp

import column_names
import config
from dataset_preprocessing.homes_datasets_preprocessing.home_data_interpolators.home_data_linear_interpolator import \
    HomeDataLinearInterpolator
from dataset_preprocessing.homes_datasets_preprocessing.home_data_parsers.soft_m_home_data_parser import \
    SoftMHomeDataParser


def process_home_dataset(home_data_interpolator, home_data_parser, home_dataset_src_path, home_dataset_dst_path):
    logging.basicConfig(level="INFO")

    home_dataset_src_path = os.path.abspath(home_dataset_src_path)
    home_dataset_dst_path = os.path.abspath(home_dataset_dst_path)

    logging.info(f"Processing {home_dataset_src_path}")
    with open(home_dataset_src_path, encoding="UTF-8") as f:
        home_df = home_data_parser.parse_home_data(f)

    home_df = home_df[
        (home_df[column_names.TIMESTAMP] >= config.START_DATETIME) &
        (home_df[column_names.TIMESTAMP] <= config.END_DATETIME)]

    home_df = home_data_interpolator.interpolate_boiler_data(
        home_df,
        start_datetime=config.START_DATETIME,
        end_datetime=config.END_DATETIME,
        inplace=True
    )
    
    logging.info(f"Saving to {home_dataset_dst_path}")
    home_df.to_pickle(home_dataset_dst_path)


def main():
    logging.basicConfig(level="DEBUG")

    home_data_parser = SoftMHomeDataParser()
    home_data_parser.set_ntc(config.NTC)
    home_data_parser.set_disabled_temp_threshold(config.HOME_DISABLED_TEMP_THRESHOLD)
    home_data_parser.set_timestamp_parse_patterns(config.HOME_TIMESTAMP_PATTERNS)
    home_data_parser.set_timestamp_timezone_name(config.HOME_DATA_TIMEZONE)
    home_data_interpolator = HomeDataLinearInterpolator()

    logging.debug(f"Searching homes datasets in {config.HOMES_SRC_DATASETS_DIR}")
    processes = []
    for dataset_name in os.listdir(config.HOMES_SRC_DATASETS_DIR):
        home_dataset_src_path = f"{config.HOMES_SRC_DATASETS_DIR}\\{dataset_name}"
        home_dataset_dst_path = f"{config.HOMES_PREPROCESSED_DATASETS_DIR}\\{dataset_name}"

        process = mp.Process(
            target=process_home_dataset,
            args=(
                home_data_interpolator,
                home_data_parser,
                home_dataset_src_path,
                home_dataset_dst_path
            )
        )
        process.start()
        processes.append(process)

    for process in processes:
        process.join()


if __name__ == '__main__':
    main()
