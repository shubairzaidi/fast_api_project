from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Body # type: ignore
from sqlalchemy.orm import Session # type: ignore
from src.database.session import get_db
from src.modules.customers import schemas,crud
from src.dependencies.dependencies import get_current_user
from src.database import models
import pandas as pd # type: ignore
from io import BytesIO

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
def get_customers(payload:schemas.GetCustomer,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.getCustomers(db,payload)

""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: To get Specific Customer"
""
@router.post("/get-customer-by-id/{customer_id}")
def get_customer_by_id(customer_id:Optional[int],db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.getCustomerById(db,customer_id)

""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: To delete Customer"
""
@router.post("/delete-customer/{customer_id}")
def delete_customer(customer_id:Optional[int],db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.deleteCustomer(db,customer_id)


""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: To update Customer"
""
@router.post("/update-customer/{customer_id}")
def update_customer(payload:schemas.UpdateCustomer,customer_id,db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.updateCustomer(db,payload,customer_id)

""
"Author:Shubair Zaidi"
"Date:28 Sept 2025",
"Purpose: Download customer list"
""
@router.post("/download")
def download_customer_Excel(db:Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    return crud.downloadCustomerExcel(db)