from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional
class PostBase(BaseModel):
    title: str
    content: str
    pulished :bool = True

class CreatePost(PostBase):
    pass

class User(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime 
    class Config:
        orm_mode = True

class Post(PostBase):
    id :int
    created_at: datetime
    own_id :int
    owner: User
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password:str

class CreateUser(UserBase):
    pass




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id : int
    dir: conint(le =1)