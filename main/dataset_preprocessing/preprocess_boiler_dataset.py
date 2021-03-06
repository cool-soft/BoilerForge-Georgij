import logging

import config
from heating_system_utils.boiler_data_interpolators.boiler_data_linear_interpolator import \
    BoilerDataLinearInterpolator
from heating_system_utils.boiler_data_parsers.soft_m_csv_boiler_data_parser import \
    SoftMCSVBoilerDataParser
from heating_system.preprocess_utils import filter_by_timestamp_closed
from heating_system_utils.constants import column_names, circuits_id

if __name__ == '__main__':
    logging.basicConfig(level="DEBUG")

    boiler_data_parser = SoftMCSVBoilerDataParser()
    boiler_data_parser.set_disabled_temp_threshold(config.BOILER_DISABLED_TEMP_THRESHOLD)
    boiler_data_parser.set_timestamp_parse_patterns(config.BOILER_TIMESTAMP_PATTERNS)
    boiler_data_parser.set_timestamp_timezone_name(config.BOILER_DATA_TIMEZONE)

    with open(config.BOILER_SRC_DATASET_PATH, encoding="UTF-8") as f:
        boiler_df = boiler_data_parser.parse_boiler_data(f)

    boiler_data_interpolator = BoilerDataLinearInterpolator()

    boiler_heating_circuit_df = boiler_df[boiler_df[column_names.CIRCUIT_ID] == circuits_id.HEATING_CIRCUIT]
    # boiler_heating_circuit_df = boiler_data_interpolator.interpolate_boiler_data(
    #     boiler_heating_circuit_df,
    #     start_datetime=config.START_DATETIME,
    #     end_datetime=config.END_DATETIME,
    #     inplace=True
    # )

    boiler_heating_circuit_df = filter_by_timestamp_closed(
        boiler_heating_circuit_df,
        config.START_DATETIME,
        config.END_DATETIME
    )

    logging.debug("Saving heating circuit df to {}".format(config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH))
    boiler_df.to_pickle(config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH)

    boiler_water_circuit_df = boiler_df[boiler_df[column_names.CIRCUIT_ID] == circuits_id.WATER_CIRCUIT]
    # boiler_water_circuit_df = boiler_data_interpolator.interpolate_boiler_data(
    #     boiler_water_circuit_df,
    #     start_datetime=config.START_DATETIME,
    #     end_datetime=config.END_DATETIME,
    #     inplace=True
    # )

    boiler_water_circuit_df = filter_by_timestamp_closed(
        boiler_water_circuit_df,
        config.START_DATETIME,
        config.END_DATETIME
    )

    logging.debug("Saving water circuit df to {}".format(config.BOILER_PREPROCESSED_WATER_CIRCUIT_DATASET_PATH))
    boiler_water_circuit_df.to_pickle(config.BOILER_PREPROCESSED_WATER_CIRCUIT_DATASET_PATH)
