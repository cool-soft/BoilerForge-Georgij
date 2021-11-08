from dependency_injector import resources
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import Engine
from sqlalchemy.orm import relationship, Session, sessionmaker, DeclarativeMeta

MetersInfoBase = declarative_base()
MeterMeasurementsBase = declarative_base()


class Boilers(MetersInfoBase):
    __tablename__ = "boilers"
    __tableargs__ = {
        "comment": "Котельные"
    }

    boiler_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True
    )
    boiler_name = Column(
        String(255),
        comment="Название котельной"
    )
    boiler_meter_ids = Column(
        String(200),
        comment="Список ID тепловычислителей, разделённых запятыми"
    )

    def __repr__(self):
        return f"{self.boiler_id} {self.boiler_name} {self.boiler_meter_ids}"


class Meters(MetersInfoBase):
    __tablename__ = "meters"
    __tableargs__ = {
        "comment": "Тепловычислители"
    }

    meter_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True
    )
    meter_name = Column(
        String(255),
        comment="Имя тепловычислителя: локальный адрес, принадлежность к типу потребителя (МКД, СОШ и т.д.)"
    )
    meter_address = Column(
        String(255),
        comment="Полный адрес, где установлен тепловычислитель"
    )
    boiler_id = Column(
        Integer,
        ForeignKey("boilers.boiler_id"),
        comment="ID котельной"
    )

    boilers = relationship(
        'Boilers',
        backref='boiler',
        lazy='subquery',
    )


class MeterMeasurements(MeterMeasurementsBase):
    __tablename__ = "meter_measurements"
    __tableargs__ = {
        "comment": "Данные с тепловычислителей"
    }
    measurement_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    d_timestamp = Column(
        DateTime,
        comment="Дата и время снятия показаний"
    )
    service = Column(
        String(10),
        comment="Обозначение услуги: ОВ / ГВС"
    )
    t1 = Column(
        Float,
        comment="Температура в подающем трубопроводе"
    )
    t2 = Column(
        Float,
        comment="Температура в обратке"
    )
    g1 = Column(
        Float,
        comment="Расход в подающем трубопроводе"
    )
    g2 = Column(
        Float,
        comment="Расход в обратке"
    )
    p1 = Column(
        Float,
        comment="Давление в подающем трубопроводе"
    )
    p2 = Column(
        Float,
        comment="Давление в обратке"
    )


class DBConnect(resources.Resource):
    _engine = None

    def init(self, path: str, base: DeclarativeMeta):
        self._engine = create_engine("sqlite:///" + path, echo=False)
        base.metadata.create_all(self._engine)
        session_factory = sessionmaker(bind=self._engine)
        return session_factory

    def shutdown(self) -> None:
        self._engine.dispose()
