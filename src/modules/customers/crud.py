from fastapi import HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import desc # type: ignore
from src.database.models import Customer
from src.modules.customers.schemas import CustomerDetails
from src.utils.helper import custom_http_response



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


def getCustomers(db:Session):
    try:
        customers = db.query(
            Customer.id.label('customer_id'),
            Customer.name,
            Customer.email,
            Customer.address
        ).order_by(desc(Customer.id)).all()

        customer_list = []
        for c in customers:
            customer_list.append({
                "customer_id":c.customer_id,
                "name":c.name,
                "email":c.email,
                "address":c.address
            })
        return custom_http_response(
        status_code=200,
        success=True,
        message="Customer created successfully",
        data=customer_list
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")