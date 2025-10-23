from sqlalchemy import Column, Integer, String, DateTime, func,Boolean,ForeignKey,Numeric,Computed,Date,Float # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import relationship


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

    vehicles = relationship("ContractorVehicle", back_populates="contractor")
    ash_contracts = relationship("AshMaster", back_populates="contractor")  
    vehicle_master = relationship('VehicleMaster', back_populates="contractor")
    contract_master = relationship('AshContractor', back_populates="contractor")


class VehicleMaster(Base):
    __tablename__ = "tbl_vehicle_master"

    id = Column(Integer, primary_key=True, index=True)
    contractor_id = Column(Integer, ForeignKey("tbl_contractor_master.id"),nullable =  False)
    vehicle_number = Column(String(50),nullable = False)
    vehicle_type = Column(String(100),nullable = True)
    capacity_tons = Column(Numeric(10, 2),nullable = True)
    status = Column(String(50),nullable = True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    contractor = relationship("ContractorMaster", back_populates="vehicle_master")

class AshMaster(Base):
    __tablename__ = "tbl_ash_contractor"

    id = Column(Integer, primary_key=True, index=True)
    contractor_id = Column(Integer, ForeignKey("tbl_contractor_master.id"),nullable =  False)
    ash_type = Column(String(50),nullable = False)
    contract_no = Column(String(100),nullable = False)
    start_date = Column(Date,nullable = False)
    end_date = Column(Date,nullable = True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    contractor = relationship("ContractorMaster", back_populates="ash_contracts")


class ContractorVehicle(Base):
    __tablename__ = "tbl_contractor_vehicle"

    id = Column(Integer, primary_key=True, index=True)
    contractor_id = Column(Integer, ForeignKey("tbl_contractor_master.id"),nullable =  False)
    vehicle_number = Column(String(50),nullable = False)
    vehicle_type = Column(String(50),nullable = True)
    capacity = Column(Float,nullable = True)
    rc_number = Column(String(100),nullable = True)
    remarks = Column(String(255),nullable = True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    contractor = relationship("ContractorMaster", back_populates="vehicles")

class AshContractor(Base):
    __tablename__ = "tbl_contract_master"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer,ForeignKey("tbl_client_master.id"),nullable=False)
    contractor_id = Column(Integer, ForeignKey("tbl_contractor_master.id"), nullable=False)
    contract_number = Column(String(100), nullable=False)
    contract_type = Column(String(100), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    total_value = Column(Numeric(18, 2), nullable=True)
    status = Column(String(50), nullable=True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    trip_details = relationship("TripDetails", back_populates="trip")
    contractor = relationship("ContractorMaster", back_populates="contract_master")

class ClientMaster(Base):
    __tablename__ = "tbl_client_master"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("tbl_company_master.id"),nullable =  False)
    client_name = Column(String(255),nullable = False)
    site_location = Column(String(255),nullable = True)
    contact_email = Column(String(255),nullable = True)
    contact_phone  = Column(String(20),nullable = True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

class CompanyMaster(Base):
    __tablename__ = "tbl_company_master"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), ForeignKey("tbl_company_master.id"),nullable =  False)
    company_type = Column(String(100),nullable = True)
    registration_number = Column(String(100),nullable = True)
    gst_number = Column(String(50),nullable = True)
    pan_number = Column(String(50),nullable = True)
    address = Column(String,nullable = True)
    contact_email = Column(String(255),nullable = True)
    contact_phone = Column(String(20),nullable = True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)



class TripDetails(Base):
    __tablename__ = "tbl_trip_details"

    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("tbl_contract_master.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("tbl_vehicle_master.id"), nullable=False)
    trip_date = Column(Date, nullable=False)
    material_type = Column(String(100), nullable=True)
    source_loaction = Column(String(255), nullable=True)
    destination_location = Column(String(255), nullable=True)
    quantity_tons = Column(Numeric(10, 2), nullable=True)
    rate_per_ton = Column(Numeric(10, 2), nullable=True)
    total_amount = Column(Numeric(10, 2), nullable=True)
    status = Column(String(50), nullable=True)
    remarks = Column(String, nullable=True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    trip = relationship("AshContractor", back_populates="trip_details")
    