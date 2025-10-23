from fastapi import APIRouter, HTTPException
from src.utils.helper import custom_http_response
from src.database.session import get_db
from src.dependencies.dependencies import get_current_user
from src.modules.contractor import crud,schemas
from src.database.models import AshContractor, ContractorMaster, ContractorVehicle, TripDetails, VehicleMaster
from sqlalchemy import func



def AddContarctors(payload,db):
    try:
        contractor = db.query(ContractorMaster).filter(ContractorMaster.contractor_name == payload.name).first()
        if contractor:
            return custom_http_response(
            status_code=200,
            success=True,
            message="Contractor already exists"
        )
        if not payload.name:
            return custom_http_response(
            status_code=200,
            success=True,
            message="Please provide a valid name of contractor"
        )
        contractor = ContractorMaster(
            contractor_name = payload.name,
            contact_phone = payload.contact_info,
            contact_email = payload.email,
            address = payload.address
        )
        db.add(contractor)
        db.commit()

        return custom_http_response(
            status_code=200,
            success=True,
            message="Contractor created successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def createContarctors(payload,db,user):
    try:
        if not payload.contractor_name:
            return custom_http_response(
            status_code=200,
            success=True,
            message="Please provide a valid name of contractor"
        )
         
        contractor = db.query(ContractorMaster).filter(ContractorMaster.contractor_name == payload.contractor_name).first()
        if contractor:
            return custom_http_response(
            status_code=200,
            success=True,
            message="Contractor already exists"
        )
        contractor = ContractorMaster(**payload.dict())
        contractor.created_by = user.id
        db.add(contractor)
        db.commit()

        return custom_http_response(
            status_code=200,
            success=True,
            message="Contractor created successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def updateContractor(schema_dict,contractor_id:int,db):
    try:
        if not contractor_id:
            return custom_http_response(
                status_code=200,
                success=True,
                message="Invalid contractot Id"
            )
        contractor = db.query(ContractorMaster).filter(ContractorMaster.id == contractor_id)
        if not contractor.first():
            return custom_http_response(
                status_code=200,
                success=True,
                message="Contractor not present"
            )
        contractor.update(schema_dict.dict(exclude_unset=True))
        db.commit()

        return custom_http_response(
            status_code=200,
            success=True,
            message="Contractor details updated successfully"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        

def getContractorDetails(req,db):
    try:
        page = max(req.page,1)
        size = max (req.size,1)

        total_count = (
            db.query(func.count(ContractorMaster.id))
            .scalar()
        )
        total_pages = (total_count + size -1) // size
        offset = (page - 1) * size

        contractor = db.query(
            ContractorMaster.id.label("contractor_id"),
            ContractorMaster.contractor_name,
            ContractorMaster.contact_phone,
            ContractorMaster.contact_email,
            ContractorMaster.address,
            ContractorMaster.license_number
        ).order_by(ContractorMaster.id.asc()).offset(offset).limit(size).all()

        contractor_details = []
        for c in contractor:
            contractor_details.append({
                "contractor_id":c.contractor_id,
                "contractor_name":c.contractor_name,
                "contact_phone":c.contact_phone,
                "contact_email":c.contact_email,
                "address":c.address,
                "license_number":c.license_number
            })

        return custom_http_response(
            status_code=200,
            success=True,
            message="Contractor details fetched successfully",
            data=contractor_details,
            total_count = total_count,
            total_pages= total_pages,
            page = page,
            size = size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def getContractorDetails(contractor_id,db):
    try:
        if not contractor_id:
            return custom_http_response(
                status_code=200,
                success=True,
                message="Invalid contractot Id"
            )
        contractor  = db.query(ContractorMaster).filter(ContractorMaster.id == contractor_id)
        if not contractor.first():
            return custom_http_response(
                status_code=200,
                success=True,
                message="Contractor not present"
            )
        contractor.delete()
        db.commit()
        return custom_http_response(
            status_code=200,
            success=True,
            message="Conractor deleted successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def tripDetails(db):
    try:
        trip_details = db.query(
            TripDetails.id.label("trip_id"),
            TripDetails.trip_date,
            TripDetails.material_type,
            TripDetails.quantity_tons,
            TripDetails.rate_per_ton,
            TripDetails.total_amount,
            TripDetails.status,
            AshContractor.contract_number,
            ContractorMaster.contractor_name,
            ContractorVehicle.vehicle_number,
            ContractorVehicle.vehicle_type
        ).outerjoin(
           AshContractor, TripDetails.contract_id == AshContractor.id
        ).outerjoin(
           VehicleMaster, TripDetails.vehicle_id == VehicleMaster.id
        ).outerjoin(
           ContractorMaster, VehicleMaster.contractor_id == ContractorMaster.id
        ).outerjoin(
           ContractorVehicle, ContractorMaster.id == ContractorVehicle.contractor_id
        ).all()
        
        if not trip_details:
            return custom_http_response(
                status_code=200,
                success=True,
                message="Details not found"
            )
        trip_data = []
        for t in trip_details:
            trip_data.append({
                "trip_id":t.trip_id,
                "trip_date":t.trip_date.strftime("%d-%m-%y"),
                "material_type":t.material_type,
                "quantity_tons": float(t.quantity_tons),
                "rate_per_ton": float(t.rate_per_ton),
                "total_amount": float(t.total_amount),
                "status":t.status,
                "contract_number":t.contract_number,
                "contractor_name":t.contractor_name,
                "vehicle_number":t.vehicle_number,
                "vehicle_type":t.vehicle_number
            })
        return custom_http_response(
            status_code=200,
            success=True,
            message="Trip details fetch successfully",
            data=trip_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



# Output should include:
# Contractor name
# Total trips completed
# Total
# Total amount (SUM of total_amount)
# Active vehicle count (DISTINCT vehicle_id)
# Latest trip date for that contractor (MAX(trip_date))
# Average trip quantity (AVG(quantity_tons))
# Month-over-month revenue change (requires subquery)

def profileSummary(db):
    try:
        profile_summary = (
            db.query(
                ContractorMaster.contractor_name,
                
            )
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


#   {
#     "contractor_name": "Green Earth Transport",
#     "total_trips": 32,
#     "total_quantity": 645.50,
#     "total_amount": 812300.00,
#     "active_vehicles": 5,
#     "latest_trip_date": "2025-10-22",
#     "avg_trip_quantity": 20.17,
#     "month_over_month_change": 12.45
#   },