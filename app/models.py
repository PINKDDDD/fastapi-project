from .database import Base
from sqlalchemy import  Boolean,Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key= True,nullable=True)
    title = Column(String,nullable= False)
    content = Column(String,nullable=False)
    pulished = Column(Boolean,server_default="True")
    created_at = Column(TIMESTAMP(timezone=True),nullable= False,server_default=text('now()'))
    own_id = Column(Integer,ForeignKey("users.id",ondelete = "CASCADE"))
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable= False,server_default=text('now()'))

class Vote(Base):
    __tablename__ = "vote"
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key= True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key= True)