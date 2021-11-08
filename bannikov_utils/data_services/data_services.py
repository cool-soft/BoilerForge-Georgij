from datetime import datetime, timedelta
from os.path import exists
from random import randrange, random
from time import sleep

from bannikov_utils.data_services.get_softm_data import get_data_from_server
from bannikov_utils.db.containers import DBContainer
from bannikov_utils.db.repository import DBRepository
from bannikov_utils.db.resources import Boilers, Meters, MeterMeasurementsBase, MeterMeasurements
from bannikov_utils.schemas import BoilerData, MeterData, MeasurementsData

PATH_TO_DBs = "c://SQLiteDBs//"


class DataServices:

    def __init__(self, db_repository: DBRepository):
        self.db_repository = db_repository

    def add_boilers(self) -> None:
        """
        Добавляем все имеющиеся котельные в БД
        :return: None
        """
        self.db_repository.clear_table(Boilers)
        params = {"method": "ai_getBoilers"}
        boilers = get_data_from_server(params=params)
        for boiler in boilers:
            json_str = str(boiler).replace("'", '"') \
                .replace("[", '"') \
                .replace("]", '"') \
                .replace("\\xa0", " ")
            boiler_data = BoilerData.parse_raw(json_str)
            self.db_repository.add_boiler(data=boiler_data)

    def add_meters(self) -> None:
        """
        Добавляем все имеющиеся тепловычислители (ПУ) в БД
        :return: None
        """
        self.db_repository.clear_table(Meters)
        boilers = self.db_repository.get_all(Boilers)
        for row in boilers:
            print(f"Получаем данные по тепловычислителям МКД, подключённых к {row.boiler_id} котельной...", end=" ")
            arguments = '{"boiler_id":' + str(row.boiler_id) + '}'
            params = {"method": "ai_getMeters", "argument": arguments}
            meter_devices = get_data_from_server(params=params, echo=False)
            print(f"Найдено {len(meter_devices)} тепловычислителей")

            if len(meter_devices) > 0:
                for meter in meter_devices:
                    json_str = str(meter).replace('"', "#") \
                        .replace("'", '"') \
                        .replace("\\xa0", " ")
                    meter_data = MeterData.parse_raw(json_str)
                    self.db_repository.add_meter(data=meter_data)

    def add_measurements(self, start: datetime, end: datetime, clear: bool = False) -> None:
        """
        Добавление полученных показаний по всем тепловычислителям (ПУ) за заданный период
        :param start: начало периода снятие показаний
        :param end: окончание периода снятия показаний
        :param clear: флаг очистки всех данных
        :return: None
        """
        meter_ids = self.get_houses_devices()
        print(f"<add_measurements>: Получен список из {len(meter_ids)} тепловычислителей МКД")
        boilers_meter_ids = self.get_boilers_devices()
        print(f"<add_measurements>: Получен список из {len(boilers_meter_ids)} тепловычислителей котельных")
        # meter_ids.extend(boilers_meter_ids)
        meter_ids = boilers_meter_ids
        if clear:
            print("<add_measurements>: Очищены данные по тепловычислителям: ")
            print("<add_measurements>: ", end=" ")
            for meter_id in meter_ids:
                self.clear_one_device_measurements(meter_id=meter_id)
            print("")

        str_end_end = end.strftime("%Y-%m-%d %H:%M:%S")
        while start < end:
            start_str = start.strftime("%Y-%m-%d %H:%M:%S")
            temp_end = start + timedelta(days=3)
            if temp_end > end:
                temp_end = end
            end_str = temp_end.strftime("%Y-%m-%d %H:%M:%S")
            print(f"<add_measurements>: Получаем данные по тепловычислителям "
                  f"[{start_str} - {end_str} / {str_end_end}]:")
            print("<add_measurements>: ", end=" ")
            for meter_id in meter_ids:
                print(meter_id, end="")
                new_records = self.add_one_device_measurements(meter_id=meter_id,
                                                               start=start_str,
                                                               end=end_str,
                                                               clear=clear)
                print(f"(+{new_records})", end=" ")

            start = temp_end
            print("")

    def add_one_device_measurements(self, meter_id: int, start: str, end: str, clear: bool) -> int:
        """
        Добавление полученных показаний по конкретному тепловычислителю (ПУ) за заданный период
        :param meter_id: номер тепловычислителя
        :param start: начало периода снятие показаний
        :param end: окончание периода снятия показаний
        :param clear: флаг очистки всех данных
        :return: количество добавленных записей в БД
        """
        arguments = '{"meter_id":' + str(meter_id) \
                    + ',"start":"' + start + '","end":"' + end + '"}'
        params = {"method": "ai_getMeterData",
                  "argument": arguments}
        measurements_rows = get_data_from_server(params=params, echo=False)

        new_records = 0
        if len(measurements_rows) > 0:
            db_container = DBContainer()
            db_params = {"path": PATH_TO_DBs + str(meter_id) + ".db",
                         "base": MeterMeasurementsBase}
            db_container.config.from_dict(db_params)
            db = db_container.db_repository()

            for measurements in measurements_rows:
                json_str = str(measurements).replace('"', "#") \
                    .replace("'", '"') \
                    .replace("\\xa0", " ")
                measurements_data = MeasurementsData.parse_raw(json_str)
                if clear:
                    db.add_measurements(measurements_data)
                    new_records += 1
                elif not db.is_measurements(measurements_data.d_timestamp, measurements_data.service):
                    db.add_measurements(measurements_data)
                    new_records += 1
        else:
            sleep(1 + randrange(0, 4) * random())

        return new_records

    def clear_one_device_measurements(self, meter_id: int) -> None:
        """
        Очистка всех данных по конкретному тепловычислителю (ПУ)
        :param meter_id: номер тепловычислителя
        :return: None
        """
        db_file = PATH_TO_DBs + str(meter_id) + ".db"
        if exists(db_file):
            db_container = DBContainer()
            db_params = {"path": db_file,
                         "base": MeterMeasurementsBase}
            db_container.config.from_dict(db_params)
            db = db_container.db_repository()
            db.clear_table(MeterMeasurements)
            print(meter_id, end=" ")

    def get_boilers_devices(self) -> list:
        """
        Получение списка тепловычислителей по всем котельным
        :return: спсиок номеров тепловычислителей
        """
        boilers = self.db_repository.get_all(Boilers.boiler_meter_ids)
        meter_ids_list = []
        for row in boilers:
            meters_ids_str: str = row.boiler_meter_ids
            if len(meters_ids_str) > 0:
                meter_ids_list.extend(list(map(int, meters_ids_str.split(","))))

        return meter_ids_list

    def get_houses_devices(self) -> list:
        """
        Получение списка тепловычислителей по всем МКД
        :return: спсиок номеров тепловычислителей
        """
        houses = self.db_repository.get_all(Meters.meter_id)
        meter_ids_list = []
        for row in houses:
            meter_ids_list.append(row.meter_id)

        return meter_ids_list
