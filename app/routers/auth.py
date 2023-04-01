from fastapi import  FastAPI, HTTPException, Response,status,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas,models,utils,oauth2
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["authentication"]
)

@router.post("/login",response_model=schemas.Token)
def login(user:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    login_user = db.query(models.User).filter(models.User.email == user.username).first()
    if not login_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = f"this {user.email} is not found")
    if not utils.verify(user.password,login_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "this password is not correct")
    
    access_token = oauth2.create_access_token(data={"user_id":login_user.id})
    return {"access_token": access_token, "token_type": "bearer"}

