import os
from datetime import datetime

import numpy as np
import pandas as pd
from boiler.constants import column_names
from boiler.data_processing.other import parse_datetime
from boiler_softm.constants.processing_parameters import HEATING_OBJ_TIMESTAMP_PARSING_PATTERNS
from dateutil.tz import gettz

import config
from bannikov_utils.data_services.containers import DataServicesContainer
from bannikov_utils.db.containers import DBContainer
from bannikov_utils.db.resources import MeterMeasurementsBase, MeterMeasurements, MetersInfoBase, Meters
from bannikov_utils.graphs import plot_heating_system_node_data
from predict_utils import plot_real_and_predicted
from train_corr_table_model import get_forward_temp, get_timedelta_in_tick, get_x_y, get_timedelta_df, get_times

START_TIMESTAMP = pd.Timestamp(year=2021, month=4, day=12, hour=23, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))
END_TIMESTAMP = pd.Timestamp(year=2021, month=5, day=12, hour=0, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))


# START_TIMESTAMP = pd.Timestamp(year=2018, month=12, day=1, hour=0, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))
# END_TIMESTAMP = pd.Timestamp(year=2019, month=6, day=1, hour=0, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))


def calc_coolant_temp_for_object(temp_correlation_df, obj_id: str, boiler_temp: float) -> float:
    temps = temp_correlation_df[
        temp_correlation_df[column_names.CORRELATED_BOILER_TEMP] <= boiler_temp
        ]
    forward_pipe_temp = temps[obj_id].max()
    return forward_pipe_temp


def plot_house_difference(house: str = "gaydara_22.pickle"):
    correlation_df = pd.read_pickle(os.path.join("../", config.TEMP_CORRELATION_TABLE_PATH))

    timedelta_df = get_timedelta_df(os.path.join("../", config.HEATING_OBJ_TIMEDELTA_PATH))

    boiler_forward_temp = get_forward_temp(
        os.path.join("../", config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH),
        START_TIMESTAMP,
        END_TIMESTAMP
    )

    dataset_name, ext = os.path.splitext(house)
    filepath = os.path.join(
        os.path.join("../", config.APARTMENT_HOUSE_PREPROCESSED_DATASETS_HEATING_CIRCUIT_DIR),
        house
    )
    apartment_house_forward_temp = get_forward_temp(filepath, START_TIMESTAMP, END_TIMESTAMP)
    heating_obj_timedelta = get_timedelta_in_tick(dataset_name, timedelta_df)
    boiler_value = boiler_forward_temp[:-heating_obj_timedelta]
    apartment_house_value = apartment_house_forward_temp[heating_obj_timedelta:]

    dates = get_times(
        os.path.join("../", config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH),
        START_TIMESTAMP,
        END_TIMESTAMP
    )
    dates = dates[heating_obj_timedelta:]

    predicted: list = []

    for boiler_temp in boiler_value:
        apartment_house_temp = calc_coolant_temp_for_object(
            temp_correlation_df=correlation_df,
            obj_id=dataset_name,
            boiler_temp=boiler_temp
        )
        predicted.append(apartment_house_temp)

    plot_real_and_predicted(
        dates=dates,
        real=apartment_house_value,
        predicted=np.array(predicted),
        who_temp="\u00B0C",
        title=house,
    )


def plot_boiler_temp():
    """
    Построение температуры теплоносителя в подающем контуре на выходе с котельной
    Данные берутся из файла pickle
    :return:
    """
    boiler_forward_temp = get_forward_temp(
        os.path.join("../", config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH),
        START_TIMESTAMP,
        END_TIMESTAMP
    )

    dates = get_times(
        os.path.join("../", config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH),
        START_TIMESTAMP,
        END_TIMESTAMP
    )

    plot_heating_system_node_data(x_data=dates, y_datas=[boiler_forward_temp],
                                  title="Температура на выходе из котельной")


def plot_house_temp(house: str = "") -> None:
    """
    Построение температуры в подающем контуре на входе в МКД теплосети
    :param house: имя файла pickle
    :return: None
    """

    start_date = pd.Timestamp(year=2021, month=1, day=1, hour=0, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))
    end_date = pd.Timestamp(year=2021, month=12, day=31, hour=0, minute=0, tz=gettz(config.DEFAULT_TIMEZONE))
    filepath = os.path.join(
        os.path.join("../", config.APARTMENT_HOUSE_PREPROCESSED_DATASETS_HEATING_CIRCUIT_DIR),
        house
    )
    apartment_house_forward_temp = get_forward_temp(filepath, start_date, end_date)

    dates = get_times(
        os.path.join("../", config.BOILER_PREPROCESSED_HEATING_CIRCUIT_DATASET_PATH),
        start_date,
        end_date
    )

    plot_heating_system_node_data(x_data=dates,
                                  y_datas=[apartment_house_forward_temp],
                                  data_labels=["Температура на входе в МКД {}"]
                                  )


def plot_house_temp_csv(house: str = ""):
    """
    Построение графика на основе данных из csv файла
    :param house: локальное имя файла
    :return: None
    """

    if house == "":
        filepath = os.path.join(
            os.path.join("../", config.APARTMENT_HOUSE_SRC_DATASETS_DIR),
        )
        listdir = os.listdir(filepath)
        file_list = list(filter(lambda x: x.endswith('.csv'), listdir))
        for file_name in file_list:
            filepath = os.path.join(
                os.path.join("../", config.APARTMENT_HOUSE_SRC_DATASETS_DIR),
                file_name
            )
            data = pd.read_csv(filepath, sep=";", encoding="utf-8")

            apartment_house_forward_temp = data["t1"]
            dates = data["d_timestamp"]
            dates = dates.apply(
                parse_datetime,
                args=(HEATING_OBJ_TIMESTAMP_PARSING_PATTERNS, gettz(config.APARTMENT_HOUSE_DATA_TIMEZONE))
            )

            plot_heating_system_node_data(x_data=dates,
                                          y_datas=[apartment_house_forward_temp],
                                          data_labels=["Температура на входе в МКД, {}"],
                                          title=file_name
                                          )
    else:
        filepath = os.path.join(
            os.path.join("../", config.APARTMENT_HOUSE_SRC_DATASETS_DIR),
            house
        )

        data = pd.read_csv(filepath, sep=";", encoding="utf-8")

        apartment_house_forward_temp = data["t1"]
        dates = data["d_timestamp"]
        dates = dates.apply(
            parse_datetime, args=(HEATING_OBJ_TIMESTAMP_PARSING_PATTERNS, gettz(config.APARTMENT_HOUSE_DATA_TIMEZONE))
        )

        plot_heating_system_node_data(x_data=dates,
                                      y_datas=[apartment_house_forward_temp],
                                      data_labels=["Температура на входе в МКД, {}"]
                                      )


def plot_from_db(meter_id: int = 144,
                 address: str = "",
                 start: datetime = datetime(2021, 9, 15, 0, 0, 0),
                 end: datetime = datetime(2021, 10, 29, 0, 0, 0),
                 data_labels: list = ["Температура на входе в МКД, {}"]
                 ):
    """Построение графиков температур теплоносителя по данным из БД
    """
    db_container = DBContainer()
    db_params = {"path": "c://SQLiteDBs//" + str(meter_id) + ".db",
                 "base": MeterMeasurementsBase}
    db_container.config.from_dict(db_params)
    db = db_container.db_repository()
    table = db.get_all(MeterMeasurements)

    if len(table) == 0:
        return -1

    for row, row_data in enumerate(table):
        new_data = row_data._sa_instance_state.dict
        for key in ["_sa_instance_state", "measurement_id"]:
            del new_data[key]
        table[row] = new_data

    df = pd.DataFrame(table)
    data = df[(df["service"] == "OV") & (df["d_timestamp"] >= start) & (df["d_timestamp"] <= end)]

    apartment_house_forward_temp = data["t1"]
    dates = data["d_timestamp"]

    plot_heating_system_node_data(x_data=dates,
                                  y_datas=[apartment_house_forward_temp],
                                  data_labels=data_labels,
                                  title=f"Тепловычислитель №{meter_id}. {address}"
                                  )
    return 0


def main():
    start_date = datetime(2021, 9, 15, 0, 0, 0)
    end_date = datetime(2021, 10, 29, 0, 0, 0)

    db_container = DBContainer()
    db_params = {"path": "c://SQLiteDBs//meters.db", "base": MetersInfoBase}
    db_container.config.from_dict(db_params)
    db_service = DataServicesContainer(db_repository=db_container.db_repository)
    services = db_service.data_services()
    meter_ids = services.get_houses_devices()
    print(f"<add_measurements>: Получен список из {len(meter_ids)} тепловычислителей МКД")
    boilers_meter_ids = services.get_boilers_devices()
    print(f"<add_measurements>: Получен список из {len(boilers_meter_ids)} тепловычислителей котельных")

    db_data = db_container.db_repository()
    meters = db_data.get_all(Meters)

    for meter in meters:
        plot_from_db(meter_id=meter.meter_id,
                     address=meter.meter_name,
                     start=start_date,
                     end=end_date)

    for meter_id in boilers_meter_ids:
        plot_from_db(meter_id=meter_id,
                     address="Котельная Центральная",
                     start=start_date,
                     end=end_date,
                     data_labels=["Температура на выходе из котельной, {}"])
    # plot_house_temp_csv()
    # plot_house_temp_csv(house="[17_OV] 17_MKD, Kommunisticheskaja, 13_.csv")
    # plot_boiler_temp()
    # plot_house_difference(house="[172_OV] 172_MKD, ul. Kommunisticheskaja, d. 11_.pickle")
    # plot_house_difference(house="[22_OV] 22_MKD, Kommunisticheskaja, 17_.pickle")
    # plot_house_difference(house="[23_OV] 23_MKD, Kommunisticheskaja, 19_.pickle")
    # plot_house_difference(house="[24_OV] 24_MKD, Kommunisticheskaja, 23_.pickle")
    # plot_house_difference(house="[25_OV] 25_MKD, Kommunisticheskaja, 25_.pickle")
    # plot_house_difference(house="[27_OV] 27_MKD, Kommunisticheskaja, 29_.pickle")
    # plot_house_difference(house="[28_OV] 28_MKD, Kommunisticheskaja, 31_.pickle")
    # plot_house_difference(house="[41_OV] 41_MKD, Lenina, 107_.pickle")
    # plot_house_difference(house="[42_OV] 42_MKD, Lenina, 109_.pickle")
    # plot_house_difference(house="[43_OV] 43_MKD, Lenina, 111_.pickle")
    # plot_house_difference(house="[44_OV] 44_MKD, Lenina, 113_.pickle")
    # plot_house_difference(house="[61_OV] 61_MKD, Jubilejnaja, 6_.pickle")


if __name__ == '__main__':
    main()
