from typing import List

from fastapi import HTTPException, APIRouter
from db.db import collection
from model.user import User

router = APIRouter()

@router.post("/", response_description="Create new user", response_model=User)
async def create_user(u: User):
    existing_user = await collection.find_one({"email": u.email})

    if existing_user != None :
        raise HTTPException(status_code=400, detail="Bad Request: User already exists")

    result = collection.insert_one(u.dict())
    u._id = str(result.inserted_id)

    return u

@router.get("/", response_description="List users", response_model=List[User])
async def read_users():
    users = await collection.find().to_list(100)

    for user in users:
        user["_id"] = str(user["_id"])

    return users

@router.get("/{email}", response_model=User)
async def read_user_by_email(email: str):
    user = await collection.find_one({"email": email})

    if user:
        return user

    raise HTTPException(status_code=404, detail="User not found")

@router.put("/{email}", response_model=User)
async def update_user(email: str, u: User):
    updated_user = await collection.find_one_and_update(
        {"email": email}, {"$set": u.dict()}
    )

    if updated_user:
        return u

    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{email}", response_model=User)
async def delete_user(email: str):
    deleted_user = await collection.find_one_and_delete({"email": email})

    if deleted_user:
        return deleted_user

    raise HTTPException(status_code=404, detail="User not found")
