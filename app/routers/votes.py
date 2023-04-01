from fastapi import APIRouter,status,Depends,HTTPException
from .. import schemas,models,utils,oauth2
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
router =  APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "Wow, post not find forever")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir==1 :
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="already voted, can not vote again")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        
        return "success add vote"
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return "success delete vote"


