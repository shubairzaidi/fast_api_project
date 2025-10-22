import shutil
from typing import Annotated, Optional
from fastapi import APIRouter, Depends,File,Form, HTTPException,UploadFile # type: ignore
from sqlalchemy.orm import Session # type: ignore
from src.database.session import get_db
from src.modules.meters import schemas,crud
from src.dependencies.dependencies import get_current_user
from src.database import models
import pandas as pd # type: ignore
from io import BytesIO
from src.utils.helper import custom_http_response
from pathlib import Path
UPLOAD_DIR = Path("src/uploads")
UPLOAD_DIR.mkdir(exist_ok=True) 



router = APIRouter()
""
"Author:Shubair Zaidi"
"Date: 4 October 2025",
"Purpose: To create metres"
""
@router.post("/install-meter")
def create_meteres(
    meter_dict: str = Form(...),
    db:Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    parsed_data = schemas.MeterDetails.validate_to_json(meter_dict)

    if not parsed_data:
        return custom_http_response(
            status_code=200,
            success=True,
            message="Invalid details"
        )
    
    request_dict = parsed_data.dict()
    return crud.install_meter(db,request_dict,current_user)


""
"Author:Shubair Zaidi"
"Date: 4 October 2025",
"Purpose: To get metres details"
""
@router.post("/meter-details")
def meter_details(
    payload :schemas.GetMeter,
    db:Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
    return crud.meterDetails(db,payload)