from fastapi import APIRouter, HTTPException
from src.utils.helper import custom_http_response
from src.database.session import get_db
from src.dependencies.dependencies import get_current_user
from src.modules.contractor import crud,schemas
from src.database.models import ContractorMaster



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

