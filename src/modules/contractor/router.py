from fastapi import APIRouter, Depends
from requests import Session
from src.database import models
from src.database.session import get_db
from src.dependencies.dependencies import get_current_user
from src.modules.contractor import crud,schemas
from src.database.models import ContractorMaster

router = APIRouter()
""
"Author:Shubair Zaidi"
"Date:22 October 2025",
"Purpose: To create contractors"
""
@router.post("/create-contractor")
def create_customers(schema_dict:schemas.CreateContractor,db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.createContarctors(schema_dict,db,current_user)


""
"Author:Shubair Zaidi"
"Date:23 October 2025",
"Purpose: To update contractors"
""
@router.post("/update-contractor/{contractor_id}")
def update_contractor(schema_dict:schemas.CreateContractor,contractor_id:int,db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.updateContractor(schema_dict,contractor_id,db)

""
"Author:Shubair Zaidi"
"Date:23 October 2025",
"Purpose: To update contractors"
""
@router.post("/contractor-details")
def contractor_details(schema:schemas.ContractorDetails,db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.getContractorDetails(schema,db)


""
"Author:Shubair Zaidi"
"Date:23 October 2025",
"Purpose: To update contractors"
""
@router.post("/delete-contractor/{contractor_id}")
def contractor_details(contractor_id,db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.getContractorDetails(contractor_id,db)