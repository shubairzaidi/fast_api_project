from typing import Annotated
from fastapi import APIRouter, Depends, Body # type: ignore
from sqlalchemy.orm import Session # type: ignore
from src.database.session import get_db
from src.modules.customers import schemas,crud
from src.dependencies.dependencies import get_current_user
from src.database import models

router = APIRouter()

""
"Author:Shubair Zaidi"
"Date:27 Sept 2025",
"Purpose: To create Customers"
""
@router.post("/create-customer")
def create_customers(schema_dict:schemas.CustomerDetails,db:Session = Depends(get_db),  current_user: models.User = Depends(get_current_user)):
    print("user ki information",current_user)
    return crud.createCustomers(schema_dict,db,current_user)


""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: To get Customers"
""
@router.post("/get-customer")
def create_customers(payload:schemas.GetCustomer,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.getCustomers(db,payload)