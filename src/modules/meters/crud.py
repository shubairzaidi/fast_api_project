from fastapi import HTTPException # type: ignore
from fastapi.responses import StreamingResponse # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import desc,func  # type: ignore
from src.database.models import Meter,Customer
from src.modules.meters.schemas import GetMeter
from src.utils.helper import custom_http_response
import pandas as pd # type: ignore
from io import BytesIO




def install_meter(db,payload,user):
    try:
        print("inside tru block")
        meter = Meter(
        meter_serial = payload["meter_serial"],
        customer_id = payload["customer_id"],
        location = payload["location"],
        installation_year = payload["installation_year"],
        is_active = payload["is_active"],  
        created_by = user.id
    )
        db.add(meter)
        db.commit()
        return custom_http_response (
            status_code=200,
            success=True,
            message="Meter installed successfully"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def meterDetails(db:Session,req:GetMeter):
    try:
        # --------- Pagination part --------------
        page = req.page  or 1
        size = req.size or 1
        page = max(page,1)
        size = max(size,1)

        # etting total_count
        total_count = (
            db.query(func.count(Meter.id))
            .scalar()
        )

        total_pages = (total_count + size - 1) // size
        offset = (page - 1 )*size

        meter = db.query(
            Meter.id.label("meter_id"),
            Meter.meter_serial,
            Meter.customer_id,
            Meter.location,
            Meter.installation_year,
            Meter.is_active   
        ).offset(offset).limit(size).all()

        meter_list = []
        for m in meter:
            meter_list.append({
                "meter_id":m.meter_id,
                "meter_serial":m.meter_serial,
                "customer_id":m.customer_id,
                "location":m.location,
                "installation_year":m.installation_year,
                "is_active":m.is_active
            })
        return custom_http_response(
            status_code= 200,
            success=True,
            message="Meter list fetched successfully",
            data=meter_list,
            total_count=total_count,
            total_pages=total_pages,
            page = page,
            size = size 
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")




