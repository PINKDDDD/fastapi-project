from typing import List,Optional
from fastapi import  FastAPI, HTTPException, Response,status,Depends,APIRouter
from .. import schemas,models,oauth2
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags= ["posts"]
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),limit:int = 10,skip:int = 0,search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts =  cursor.fetchall() 
    #posts = db.query(models.Post).filter(models.Post.own_id == current_user.id).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search))
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id ,isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts 

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(name:schemas.CreatePost,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title,content,pulished) values(%s,%s,%s) RETURNING * """,(name.title,name.content,name.pulished))
    # post = cursor.fetchone()
    # conn.commit()
    
    post = models.Post(own_id = current_user.id,**name.dict())
    print(current_user.email)
    db.add(post)
    db.commit()
    db.refresh(post)
    return  post 

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id),))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Wow, not find forever")
    return post

@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    # post = cursor.fetchone()
    # conn.commit
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Wow, No id {id} post able to delete")
    if post.own_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = f"Wow, No authorized to delete")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,name:schemas.CreatePost,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title= %s,content= %s,pulished=  %s WHERE id = %s RETURNING * """,(name.title,name.content,name.pulished,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Wow, No id {id} post able to change")
    if post.own_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = f"Wow, No authorized to change")
    post_query.update(name.dict(),synchronize_session=False) 
    db.commit()
    return post