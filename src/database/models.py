from sqlalchemy import Column, Integer, String, DateTime, func,Boolean # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore


Base = declarative_base() 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    address = Column(String(200),nullable=True)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=True)
    email = Column(String(100), nullable=True)
    profile_photo = Column(String(255),nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True, index=True)
    meter_serial = Column(String(50),nullable= True)
    customer_id = Column(Integer,nullable = True)
    location = Column(String(150),nullable= True)
    installation_year = Column(Integer,nullable= True)
    is_active = Column(Boolean,nullable= True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class ContractorMaster(Base):
    __tablename__ = "tbl_contractor_master"

    id = Column(Integer, primary_key=True, index=True)
    contractor_name = Column(String(255),nullable= False)
    license_number = Column(String(100),nullable = True)
    contact_email = Column(String(255),nullable= True)
    contact_phone = Column(String(20),nullable= True)
    address = Column(String(50),nullable= True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)



