from fastapi import FastAPI, HTTPException
from db.db import client
from controller.userCRUD import router as user_router

app = FastAPI()
app.include_router(user_router, tags=["users"], prefix="/users")
# MongoDB connection URL
@app.on_event("shutdown")
def shutdown_db_client():
    client.close()
