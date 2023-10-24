from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, DECIMAL, Date, Table, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from ..database.database import Base


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(20), unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_login = Column(DateTime)

    role_id = Column(Integer, ForeignKey('roles.role_id'))

    role = relationship("Role")


class Location(Base):
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    address = Column(String(255))
    phone = Column(String(15))
    start_time = Column(String(50))
    end_time = Column(String(50))
    coordinates = Column(String(50))


class Barber(Base):
    __tablename__ = "barbers"
    barber_id = Column(Integer, primary_key=True, autoincrement=True)
    bio = Column(Text)
    specialization = Column(String)
    profile_picture = Column(String)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, unique=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'), nullable=True)

    user = relationship("User")
    location = relationship("Location")


class Service(Base):
    __tablename__ = 'services'

    service_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    duration = Column(Integer)
    price = Column(DECIMAL(10, 2))
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    description = Column(Text)

    location = relationship("Location")


class Inventory(Base):
    __tablename__ = 'inventory'

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    product_name = Column(String(100))
    quantity = Column(Integer)
    last_restocked = Column(DateTime)

    location = relationship("Location")


appointment_timeslot_association = Table(
    'appointment_timeslot_association',
    Base.metadata,
    Column('appointment_id', Integer, ForeignKey('appointments.appointment_id')),
    Column('time_slot_id', Integer, ForeignKey('timeSlots.slot_id'))
)


class Appointment(Base):
    __tablename__ = 'appointments'

    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    barber_id = Column(Integer, ForeignKey('barbers.barber_id'))
    service_id = Column(Integer, ForeignKey('services.service_id'))
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    appointment_time = Column(TIMESTAMP)
    status = Column(String(20))
    special_request = Column(Text)

    user = relationship("User")
    barber = relationship("Barber")
    service = relationship("Service")
    location = relationship("Location")
    time_slots = relationship('TimeSlot', secondary=appointment_timeslot_association, back_populates='appointments')


class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    barber_id = Column(Integer, ForeignKey('barbers.barber_id'))
    rating = Column(Integer)
    review_text = Column(Text)
    created_at = Column(TIMESTAMP)

    user = relationship("User")
    barber = relationship("Barber")


class Promotion(Base):
    __tablename__ = 'promotions'

    promotion_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    discount_type = Column(String(50))
    discount_value = Column(DECIMAL(10, 2))


class Payment(Base):
    __tablename__ = 'payments'

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    appointment_id = Column(Integer, ForeignKey('appointments.appointment_id'))
    amount = Column(DECIMAL(10, 2))
    payment_method = Column(String(50))
    payment_time = Column(TIMESTAMP)

    user = relationship("User")
    appointments = relationship("Appointment")


class TimeSlot(Base):
    __tablename__ = 'timeSlots'

    slot_id = Column(Integer, primary_key=True, autoincrement=True)
    barber_id = Column(Integer, ForeignKey('barbers.barber_id'))
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)
    availability = Column(Boolean, default=True)

    barbers = relationship("Barber")

    appointments = relationship('Appointment', secondary=appointment_timeslot_association, back_populates='time_slots')

    def update_availability(self, new_availability):
        self.availability = new_availability
