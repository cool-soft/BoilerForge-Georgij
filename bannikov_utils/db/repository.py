from datetime import datetime

from boiler_softm.constants.processing_parameters import HEATING_OBJ_TIMESTAMP_PARSING_PATTERNS
from dateutil.tz import gettz

import config

from bannikov_utils.db.resources import Boilers, Meters, MeterMeasurements
from bannikov_utils.schemas import BoilerData, MeterData, MeasurementsData
from bannikov_utils.utils.date_time_utils import parse_datetime_sec


class DBRepository:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def clear_table(self, table) -> None:
        """
        Очистка всей таблицы
        :param table: таблица
        :return: None
        """
        with self.session_factory() as session:
            rows = self.get_all(table)
            for row in rows:
                session.delete(row)
            session.commit()

    def get_all(self, table):
        """
        Возвращает содержимое всей таблицы
        :param table: таблица
        :return: все строки таблицы
        """
        with self.session_factory() as session:
            rows = session.query(table).all()
        return rows

    def add_boiler(self, data: BoilerData) -> None:
        with self.session_factory() as session:
            session.add(Boilers(boiler_id=data.boiler_id,
                                boiler_name=data.boiler_name,
                                boiler_meter_ids=data.boiler_meter_ids
                                ))
            session.commit()

    def add_meter(self, data: MeterData) -> None:
        with self.session_factory() as session:
            session.add(Meters(meter_id=data.meter_id,
                               meter_name=data.meter_name,
                               meter_address=data.meter_address,
                               boiler_id=data.boiler_id
                               ))
            session.commit()

    def add_measurements(self, data: MeasurementsData) -> None:
        with self.session_factory() as session:
            session.add(MeterMeasurements(d_timestamp=data.d_timestamp,
                                          service=data.service,
                                          t1=data.t1,
                                          t2=data.t2,
                                          g1=data.g1,
                                          g2=data.g2,
                                          p1=data.p1,
                                          p2=data.p2
                                          ))
            session.commit()

    def is_measurements(self, d_timestamp: datetime, service: str) -> bool:
        """
        Проверка суествования в БД записи по снятым показаниям тепловычислителей
        :param d_timestamp: дата и время снятия показаний
        :param service: поставляемая услуга OV / GVS
        :return: True - запись существует, False - запись не найдена
        """
        with self.session_factory() as session:
            mesurements = session.query(MeterMeasurements) \
                .filter(MeterMeasurements.d_timestamp == d_timestamp) \
                .filter(MeterMeasurements.service == service) \
                .all()
        return len(mesurements) > 0
