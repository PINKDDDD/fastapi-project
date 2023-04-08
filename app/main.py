from fastapi import  FastAPI
from .routers import posts,users,auth,votes
from. import models
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
# from fastapi import  FastAPI, HTTPException, Response,status,Depends
# from typing import List, Optional
# from fastapi.params import Body
# from . import schemas,utils
# from sqlalchemy.orm import Session
# from .database import engine,SessionLocal,get_db
# import psycopg2
# from psycopg2.extras import RealDictCursor

#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "Hello World!!"}



    