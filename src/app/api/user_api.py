from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

from models.user_model import User, UserRequest, UserResponse
from utils.validate import validate_username, validate_password

router = APIRouter()


@router.post("/create", response_model=UserResponse, description="To create a user account with password")
async def create_user(user: UserRequest):
    try:
        existing_user = await User.find_one({"username": user.username})

        if existing_user:
            raise Exception("User already exists")

        validate_username(user.username)
        validate_password(user.password)
        await User(username=user.username, password=user.password).insert()

        return JSONResponse({"success": True}, 201)
    except Exception as e:
        logging.info(f"[post_create] {user} failed with error {e}")
        return JSONResponse({"success": False, "reason" : str(e)}, 400)


@router.post("/verify", response_model=UserResponse, description="To verify account and password")
async def verify_user(user: UserRequest):
    # Verify user exists
    existing_user = await User.find_one({"username": user.username})
    if not existing_user:
        return JSONResponse({"success": False, "reason": "User doesn't exists, please create your account first"}, 400)

    if user.password != existing_user.password:
        if existing_user.incorrect_password_attempts == 5:
            time_difference = int((datetime.now() - existing_user.lockout_timestamp).total_seconds())
            if time_difference > 59:
                # Reset attempts
                existing_user = await existing_user.update({"$set": {"incorrect_password_attempts": 1}})
                return JSONResponse({"success": False, "reason": "Incorrect password. Please try again."}, 400)
            else:
                # Display remaining time
                remaining_time = 60 - time_difference
                return JSONResponse({"success": False, "reason": f"Too many incorrect attempts. Please wait for {remaining_time} seconds before trying again."}, 429)

        if existing_user.incorrect_password_attempts == 4:
            # Update lockout_time for 5th attempt
            await existing_user.update({"$inc": {"incorrect_password_attempts": 1}, "$set": {"lockout_timestamp": datetime.now()}})
        else:
            await existing_user.update({"$inc": {"incorrect_password_attempts": 1}})
        return JSONResponse({"success": False, "reason": "Incorrect password. Please try again."}, 400)

    return JSONResponse({"success": True}, 200)
