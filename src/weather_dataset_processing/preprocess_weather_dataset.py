
import os
import logging

import config
from weather_dataset_processing.weather_data_interpolators.weather_data_linear_interpolator import \
    WeatherDataLinearInterpolator
from weather_dataset_processing.weather_data_parsers.soft_m_weather_data_parser import \
    SoftMWeatherDataParser


def process_weather_dataset():
    with open(os.path.abspath(config.SRC_WEATHER_DATASET_PATH), "r") as f:
        weather_data = f.read()

    parser = SoftMWeatherDataParser()
    parser.set_weather_data_timezone_name(config.WEATHER_DATA_TIMEZONE)
    weather_df = parser.parse_weather_data(weather_data)

    interpolator = WeatherDataLinearInterpolator()
    interpolator.interpolate_weather_data(weather_df, config.START_DATE, config.END_DATE, inplace=True)

    weather_df.to_pickle(config.PREPROCESSED_WEATHER_DATASET_PATH)


if __name__ == '__main__':
    logging.basicConfig(level="DEBUG")
    process_weather_dataset()
