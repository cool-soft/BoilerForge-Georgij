import json
from datetime import datetime, timedelta

from boiler.data_processing.other import parse_datetime
from boiler_softm.constants.processing_parameters import HEATING_OBJ_TIMESTAMP_PARSING_PATTERNS
from dateutil.tz import gettz

import config
from bannikov_utils.db.containers import DBContainer
from bannikov_utils.db.repository import DBRepository
from bannikov_utils.db.resources import MetersInfoBase, MeterMeasurementsBase, Boilers, Meters, MeterMeasurements, \
    DBConnect
from bannikov_utils.schemas import BoilerData, MeterData, MeasurementsData

if __name__ == '__main__':
    boiler = '{"boiler_id": 1, "boiler_name": "Котельная Центральная", "boiler_meter_ids": "144, 155"}'
    boiler = "{'boiler_id': 1, 'boiler_name': 'Котельная Центральная', 'boiler_meter_ids': '144, 156'}"
    boiler_data = BoilerData.parse_raw(boiler.replace("'", '"'))

    meter = '{"meter_id": 1, "meter_name": "МКД, Банковский пер., 3", ' \
            '"meter_address": "г Чернушка, пер Банковский, дом 3", "boiler_id": 1}'
    meter_data = MeterData.parse_raw(meter)

    db_container = DBContainer()
    db_params = {"path": "d://SQLiteDBs//meters.db", "base": MetersInfoBase}
    db_container.config.from_dict(db_params)
    db = db_container.db_repository()
    #db.clear_table(Boilers)
    #db.add_boiler(data=boiler_data)
    #db.clear_table(Meters)
    #db.add_meter(data=meter_data)

    meter_measurements = '{"d_timestamp": "2021-10-14 00:00:02", ' \
                         '"service": "OV", ' \
                         '"t1": 11169.86, "t2": 58.37, ' \
                         '"g1": 1885.59, "g2": 1668.5, ' \
                         '"p1": 5.04, "p2": 2.58}'
    measurements_data = MeasurementsData.parse_raw(meter_measurements)
    db_container = DBContainer()
    db_params = {"path": "d://SQLiteDBs//145.db", "base": MeterMeasurementsBase}
    db_container.config.from_dict(db_params)
    db = db_container.db_repository()

    #db.clear_table(MeterMeasurements)
    d_timestamp = datetime(2021, 10, 14, 0, 0, 2, tzinfo=gettz(config.DEFAULT_TIMEZONE))
    d_timestamp = d_timestamp + timedelta(days=1)
    if not db.is_measurements(d_timestamp=d_timestamp):
        db.add_measurements(measurements_data)

    # mj = json.loads(meter_measurements)
    # d = parse_datetime(datetime_as_str=mj["d_timestamp"],
    #                    datetime_patterns=HEATING_OBJ_TIMESTAMP_PARSING_PATTERNS,
    #                    timezone=gettz(config.BOILER_DATA_TIMEZONE))
    # mj["d_timestamp"] = str(d)
    # measurements_data = MeasurementsData.parse_raw(str(mj).replace("'", '"'))

