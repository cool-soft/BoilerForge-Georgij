import logging

import column_names
import config
from dataset_preprocessing.boiler_dataset_preprocessing.boiler_data_interpolators.boiler_data_linear_interpolator import \
    BoilerDataLinearInterpolator
from dataset_preprocessing.boiler_dataset_preprocessing.boiler_data_parsers.soft_m_boiler_data_parser import \
    SoftMBoilerDataParser
from preprocess_utils import filter_by_timestamp_closed

if __name__ == '__main__':
    logging.basicConfig(level="DEBUG")

    boiler_data_parser = SoftMBoilerDataParser()
    boiler_data_parser.set_ntc(config.NTC)
    boiler_data_parser.set_disabled_temp_threshold(config.BOILER_DISABLED_TEMP_THRESHOLD)
    boiler_data_parser.set_timestamp_parse_patterns(config.BOILER_TIMESTAMP_PATTERNS)
    boiler_data_parser.set_timestamp_timezone_name(config.BOILER_DATA_TIMEZONE)

    with open(config.BOILER_SRC_DATASET_PATH, encoding="UTF-8") as f:
        boiler_df = boiler_data_parser.parse_boiler_data(f)

    boiler_data_interpolator = BoilerDataLinearInterpolator()
    boiler_df = boiler_data_interpolator.interpolate_boiler_data(
        boiler_df,
        start_datetime=config.START_DATETIME,
        end_datetime=config.END_DATETIME,
        inplace=True
    )

    boiler_df = filter_by_timestamp_closed(boiler_df, config.START_DATETIME, config.END_DATETIME)

    logging.debug("Saving to {}".format(config.BOILER_PREPROCESSED_DATASET_PATH))
    boiler_df.to_pickle(config.BOILER_PREPROCESSED_DATASET_PATH)
