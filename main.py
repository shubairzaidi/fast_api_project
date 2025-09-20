from fastapi import FastAPI,Depends
from src.modules.vendor.router import router as vendor_router
from src.database.session import Base, engine
from src.dependencies.auth import create_access_token
from src.dependencies.dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Project")
@app.post("/token")
def get_token():
    # Normally validate user credentials, but here just return JWT
    token = create_access_token({"sub": "test_user"})
    print(token)
    return {"access_token": token, "token_type": "bearer"}

app.include_router(vendor_router, prefix="/vendor", tags=["Vendor"],dependencies=[Depends(get_current_user)])

@app.get("/")
def root():
    return {"message": "FastAPI Project Running"}
