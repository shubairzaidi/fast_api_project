from fastapi import HTTPException # type: ignore
from fastapi.responses import StreamingResponse # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import desc,func  # type: ignore
from src.database.models import Customer
from src.modules.customers.schemas import CustomerDetails,GetCustomer,UpdateCustomer
from src.utils.helper import custom_http_response
import pandas as pd # type: ignore
from io import BytesIO


def createCustomers(schema_dict:CustomerDetails ,db:Session,user):
    try:
        customer = db.query(Customer).filter(Customer.name  == schema_dict.name).first()
        if customer:
           return custom_http_response(
            status_code=200,
            success=True,
            message="Customer alredy exits"
        )
        customer = Customer(
            name = schema_dict.name,
            address = schema_dict.address,
            email = schema_dict.email,
            created_by=user.id,
        )
        db.add(customer)
        db.commit()
        return custom_http_response(
            status_code=200,
            success=True,
            message="Customer created successfully"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def getCustomers(db:Session,req:GetCustomer):
    try:
        # --------- Pagination part --------------
        page = req.page or 1
        size = req.size or 1
        page = max(page,1)
        size = max(size,1)

        # getting total_count
        total_count = (
            db.query(func.count(Customer.id))
            .scalar()
        )
        total_pages = (total_count + size - 1)//size
        offset = (page - 1)*size
        customers = db.query(
            Customer.id.label('customer_id'),
            Customer.name,
            Customer.email,
            Customer.address
        ).order_by(desc(Customer.id)
        ).offset(offset).limit(size).all()

        customer_list = []
        for c in customers:
            customer_list.append({
                "customer_id":c.customer_id,
                "name":c.name,
                "email":c.email,
                "address":c.address,
            })
        return custom_http_response(
        status_code=200,
        success=True,
        message="Customer created successfully",
        data=customer_list,
        total_count=total_count,
        total_pages=total_pages,
        page = page,
        size = size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

def getCustomerById(db:Session,customer_id:int):
    try:
        if not customer_id:
            return custom_http_response(
            status_code=200,
            success=True,
            message="Invalid customer id"
        ) 
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
           return custom_http_response(
            status_code=200,
            success=True,
            message="Customer not found"
        ) 
        return custom_http_response(
            status_code=200,
            success=True,
            message="Customer fetch successfully",
            data=customer
        ) 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

def deleteCustomer(db:Session,customer_id:int):
    try:
        if not customer_id:
            return custom_http_response(
                status_code=200,
                success=True,
                message="Invalid customer Id"
            )
        if customer_id:
            db.query(Customer).filter(Customer.id  == customer_id).delete()
            
        return custom_http_response(
            status_code=200,
            success=True,
            message="Customer deleted successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
def updateCustomer(db:Session,req:UpdateCustomer,customer_id:int):
    try:
        if not customer_id:
            return custom_http_response(
                status_code=200,
                success=False,
                message="Invalid customer Id"
            )
        
        if not req.name and req.email:
            return custom_http_response(
                status_code=200,
                success=False,
                message="Invalid name or email"
            )
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return custom_http_response(
                status_code=200,
                success=False,
                message="Customer not found"
            )
        customer.name = req.name
        customer.email = req.email
        customer.address = req.address

        db.commit()
        db.refresh(customer)

        return custom_http_response(
                status_code=200,
                success=True,
                message="Customer updated successfully"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def downloadCustomerExcel(db:Session):
    try:
        customers = db.query(Customer).all()
        data = []

        for c in customers:
            data.append({
                "name":c.name,
                "email":c.email,
                "address":c.address
            })

        # Create a data frame
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Customers")
        output.seek(0)

        # Send as response
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=customers.xlsx"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
# add customers using forms
def addCustomer(db: Session, request: dict,user):
    try:
        existing = db.query(Customer).filter(
            (Customer.name == request.get("name"))).first()

        if existing:
            return custom_http_response(
                status_code=200,
                success=False,
                message="Customer already exists"
            )

        # Create new customer object
        customer = Customer(
            name=request.get("name"),
            email=request.get("email"),
            address=request.get("address"),
            profile_photo=request.get("profile_photo"),
            created_by=user.id,
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return custom_http_response(
            status_code=200,
            success=True,
            message="Customer added successfully"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")