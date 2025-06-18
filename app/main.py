from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/identify", response_model=schemas.IdentifyResponse)
def identify_contact(request: schemas.IdentifyRequest, db: Session = Depends(get_db)):
    if not request.email and not request.phoneNumber:
        raise HTTPException(status_code=400, detail="Either email or phoneNumber must be provided")

    result = crud.consolidate_contacts(request.email, request.phoneNumber, db)
    return {"contact": result}
