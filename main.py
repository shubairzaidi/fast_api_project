from datetime import timedelta
from fastapi import FastAPI,Depends
from src.modules.vendor.router import router as vendor_router
from src.modules.customers.router import router as customers
from src.modules.meters.router import router as meter
from src.database.session import Base, engine
from src.dependencies.auth import create_access_token
from src.dependencies.dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Project")
@app.post("/token")
def get_token():
    token = create_access_token({"sub": 1}, expires_delta=timedelta(hours=1))
    return {"access_token": token, "token_type": "bearer"}

app.include_router(vendor_router, prefix="/vendor", tags=["Vendor"],dependencies=[Depends(get_current_user)])
app.include_router(customers, prefix="/customers", tags=["Customer"],dependencies=[Depends(get_current_user)])
app.include_router(meter, prefix="/meter", tags=["Meter"],dependencies=[Depends(get_current_user)])


