from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Таблица для связи многие-ко-многим между Организациями и Деятельностями
organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)
#
# # Таблица для связи многие-ко-многим между Организациями и Телефонами
# organization_phone = Table(
#     'organization_phone',
#     Base.metadata,
#     Column('organization_id', Integer, ForeignKey('organizations.id')),
#     Column('phone_id', Integer, ForeignKey('phones.id'))
# )


class Building(Base):
    """Модель Здания"""
    __tablename__ = 'buildings'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(500), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)  # Широта
    longitude = Column(Float, nullable=False)  # Долгота

    # Связь с организациями
    organizations = relationship("Organization", back_populates="building", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Building {self.address}>"


class Phone(Base):
    """Модель Телефона"""
    __tablename__ = 'phones'

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Phone {self.phone_number}>"


class Activity(Base):
    """Модель Деятельности с поддержкой древовидной структуры"""
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    level = Column(Integer, default=1)  # Уровень вложенности
    parent_id = Column(Integer, ForeignKey('activities.id'), nullable=True)

    # Рекурсивная связь для древовидной структуры
    parent = relationship("Activity", remote_side=[id], back_populates="children")
    children = relationship("Activity", back_populates="parent", cascade="all, delete-orphan")

    # Связь с организациями
    organizations = relationship(
        "Organization",
        secondary=organization_activity,
        back_populates="activities"
    )

    def __repr__(self):
        return f"<Activity {self.name} (Level: {self.level})>"


class Organization(Base):
    """Модель Организации"""
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    building_id = Column(Integer, ForeignKey('buildings.id'), nullable=False)

    # Связи
    building = relationship("Building", back_populates="organizations")

    activities = relationship(
        "Activity",
        secondary=organization_activity,
        back_populates="organizations"
    )

    # phones = relationship(
    #     "Phone",
    #     secondary=organization_phone,
    #     cascade="all, delete"
    # )

    def __repr__(self):
        return f"<Organization {self.name}>"