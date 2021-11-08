from datetime import datetime

from dateutil.tz import gettz

import config
from bannikov_utils.data_services.containers import DataServicesContainer
from bannikov_utils.db.containers import DBContainer
from bannikov_utils.db.resources import MetersInfoBase

if __name__ == '__main__':

    db_container = DBContainer()
    db_params = {"path": "d://SQLiteDBs//meters.db", "base": MetersInfoBase}
    db_container.config.from_dict(db_params)

    db_service = DataServicesContainer(db_repository=db_container.db_repository)
    services = db_service.data_services()
    # services.add_boilers()
    # services.add_meters()

    start_date = datetime(2021, 9, 1, 0, 0, 0, tzinfo=gettz(config.DEFAULT_TIMEZONE))
    end_date = datetime(2021, 10, 29, 0, 0, 0, tzinfo=gettz(config.DEFAULT_TIMEZONE))
    services.add_measurements(start=start_date, end=end_date, clear=False)
