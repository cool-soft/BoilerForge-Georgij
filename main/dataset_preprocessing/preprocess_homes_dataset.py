import logging
import multiprocessing as mp
import os

from heating_system.preprocess_utils import filter_by_timestamp_closed
from heating_system_utils.heating_system_data_interpolators.heating_system_data_linear_interpolator \
    import HeatingSystemDataLinearInterpolator
from heating_system_utils.heating_system_data_parsers.soft_m_csv_heating_system_data_parser \
    import SoftMCSVHeatingSystemDataParser
from heating_system_utils.constants import column_names, circuits_id
from main import config


def process_home_dataset(home_data_interpolator, home_data_parser, home_dataset_src_path, home_dataset_dst_path):
    logging.basicConfig(level="INFO")

    home_dataset_src_path = os.path.abspath(home_dataset_src_path)
    home_dataset_dst_path = os.path.abspath(home_dataset_dst_path)

    logging.info(f"Processing {home_dataset_src_path}")

    with open(home_dataset_src_path, encoding="UTF-8") as f:
        home_df = home_data_parser.parse(f)

    home_heating_circuit_df = home_df[home_df[column_names.CIRCUIT_ID] == circuits_id.HEATING_CIRCUIT].copy()
    del home_heating_circuit_df[column_names.CIRCUIT_ID]
    home_heating_circuit_df = home_data_interpolator.interpolate_data(
        home_heating_circuit_df,
        start_datetime=config.START_DATETIME,
        end_datetime=config.END_DATETIME,
        inplace=True
    )
    home_heating_circuit_df = filter_by_timestamp_closed(
        home_heating_circuit_df,
        config.START_DATETIME,
        config.END_DATETIME
    )
    logging.debug("Saving heating circuit df to {}".format(home_dataset_dst_path))
    home_heating_circuit_df.to_pickle(home_dataset_dst_path)


def main():
    logging.basicConfig(level="DEBUG")

    home_data_parser = SoftMCSVHeatingSystemDataParser()
    home_data_parser.set_timestamp_parse_patterns(config.HOME_TIMESTAMP_PATTERNS)
    home_data_parser.set_timestamp_timezone_name(config.HOME_DATA_TIMEZONE)
    home_data_parser.set_need_circuits(config.HOME_REQUIRED_CIRCUITS)
    home_data_parser.set_need_columns(config.HOME_REQUIRED_COLUMNS)
    home_data_parser.set_need_to_float_convert_columns(config.HOME_NEED_TO_FLOAT_CONVERT_COLUMNS)

    home_data_interpolator = HeatingSystemDataLinearInterpolator()
    home_data_interpolator.set_interpolation_step(config.TIME_TICK)
    home_data_interpolator.set_columns_to_interpolate(config.HOME_COLUMNS_TO_INTERPOLATE)

    logging.debug(f"Searching homes datasets in {config.HOMES_SRC_DATASETS_DIR}")
    processes = []
    for dataset_name in os.listdir(config.HOMES_SRC_DATASETS_DIR):
        home_dataset_src_path = f"{config.HOMES_SRC_DATASETS_DIR}\\{dataset_name}"
        home_dataset_dst_path = f"{config.HOMES_PREPROCESSED_HEATING_CIRCUIT_DATASETS_DIR}\\" \
                                f"{dataset_name}{config.PREPROCESSED_DATASET_FILENAME_EXT}"

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
