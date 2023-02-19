from boiler.constants import column_names

import config
from boiler.weather.io.sync_weather_file_loader import SyncWeatherFileLoader
from boiler_softm_lysva.weather.io import SoftMLysvaSyncWeatherForecastOnlineReader
from boiler.weather.io.sync_weather_pickle_writer import SyncWeatherPickleWriter
from boiler.weather.io.sync_weather_file_dumper import SyncWeatherFileDumper
from boiler_softm_lysva.weather.processing import SoftMLysvaWeatherForecastProcessor


if __name__ == '__main__':
    reader = SoftMLysvaSyncWeatherForecastOnlineReader()
    loader = SyncWeatherFileLoader(f"{config.WEATHER_SRC_DATASET_PATH}", reader)
    weather_df = loader.load_weather()

    processor = SoftMLysvaWeatherForecastProcessor()
    weather_df = processor.process_weather_df(
        weather_df,
        weather_df[column_names.TIMESTAMP].min(),
        weather_df[column_names.TIMESTAMP].max()
    )

    writer = SyncWeatherPickleWriter()
    dumper = SyncWeatherFileDumper(config.WEATHER_PREPROCESSED_DATASET_PATH, writer)
    dumper.dump_weather(weather_df)
