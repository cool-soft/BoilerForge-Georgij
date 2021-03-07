import logging

from main import config
from heating_system import time_tick
from heating_system_utils.boiler_data_interpolators.boiler_data_linear_interpolator import \
    BoilerDataLinearInterpolator
from heating_system_utils.boiler_data_parsers.soft_m_csv_boiler_data_parser import \
    SoftMCSVBoilerDataParser
from heating_system.preprocess_utils import filter_by_timestamp_closed
from heating_system_utils.constants import column_names, circuits_id


def main():
    logging.basicConfig(level="DEBUG")

    boiler_data_parser = SoftMCSVBoilerDataParser()
    boiler_data_parser.set_timestamp_parse_patterns(config.BOILER_TIMESTAMP_PATTERNS)
    boiler_data_parser.set_timestamp_timezone_name(config.BOILER_DATA_TIMEZONE)
    boiler_data_parser.set_need_circuits(config.BOILER_REQUIRED_CIRCUITS)
    boiler_data_parser.set_need_columns(config.BOILER_REQUIRED_COLUMNS)
    boiler_data_parser.set_need_to_float_convert_columns(config.BOILER_NEED_TO_FLOAT_CONVERT_COLUMNS)

    boiler_data_interpolator = BoilerDataLinearInterpolator()
    boiler_data_interpolator.set_interpolation_step(time_tick.TIME_TICK)
    boiler_data_interpolator.set_columns_to_interpolate(config.BOILER_COLUMNS_TO_INTERPOLATE)

    with open(config.BOILER_SRC_DATASET_PATH, encoding="UTF-8") as f:
        boiler_df = boiler_data_parser.parse(f)

    boiler_heating_circuit_df = boiler_df[boiler_df[column_names.CIRCUIT_ID] == circuits_id.HEATING_CIRCUIT].copy()
    del boiler_heating_circuit_df[column_names.CIRCUIT_ID]
    boiler_heating_circuit_df = boiler_data_interpolator.interpolate_data(
        boiler_heating_circuit_df,
        start_datetime=config.START_DATETIME,
        end_datetime=config.END_DATETIME,
        inplace=True
    )
    boiler_heating_circuit_df = filter_by_timestamp_closed(
        boiler_heating_circuit_df,
        config.START_DATETIME,
        config.END_DATETIME
    )
    logging.debug("Saving heating circuit df to {}".format(config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH))
    boiler_heating_circuit_df.to_pickle(config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH)


if __name__ == '__main__':
    main()
