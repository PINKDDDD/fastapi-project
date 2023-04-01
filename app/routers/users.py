from typing import List
from fastapi import  FastAPI, HTTPException, Response,status,Depends,APIRouter
from .. import schemas,models,utils
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.User)
def create_user(user:schemas.CreateUser,db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user 
@router.get("/{id}",response_model=schemas.User)
def get_user(id:int,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Wow, No id {id} user is able to show")
    return user.first()