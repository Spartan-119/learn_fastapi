# user related endpoints (registration and login)

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import crud, schemas, auth, models

router = APIRouter()

@router.post("/register", response_model = schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    return crud.create_user(db = db, user = user)

@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
               db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code = 400, detail = "Invalid Credentials!!!")
    access_token = auth.create_access_token(date = {"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}