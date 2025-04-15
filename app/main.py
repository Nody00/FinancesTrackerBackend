from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, engine
import models
from routers import router as api_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router, prefix="/api")


@app.get("/users", status_code=200)
async def get_users(db: Session = Depends(get_db)):
    items = db.query(models.User).all()
    return {"users": items}
