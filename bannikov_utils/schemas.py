from datetime import datetime
from pydantic import BaseModel


class BoilerData(BaseModel):
    boiler_id: int
    boiler_name: str
    boiler_meter_ids: str


class MeterData(BaseModel):
    meter_id: int
    meter_name: str
    meter_address: str
    boiler_id: int


class MeasurementsData(BaseModel):
    d_timestamp: datetime
    service: str
    t1: float = None
    t2: float = None
    g1: float = None
    g2: float = None
    p1: float = None
    p2: float = None
