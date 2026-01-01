from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> dict:
    return {"message": "Hello root"}


# PATH PARAMETER:
@app.get("/greet/{user_name}")
async def greet_user(user_name: str) -> dict:
    return {"message": f"Welcome back {user_name}"}


# QUERY PARAMETER:
@app.get("/goodbye")
async def say_bye(user_name):
    return {"message": f"Have a good day, {user_name}!"}


# MIX BOTH PATH AND QUERY PARAMS
@app.get("/has_id/{user_name}")
async def has_id(user_name: str, age: int):
    if age >= 18:
        return {"message": f"{user_name}, your ID is valid", "has_id": True}
    else:
        return {"message": f"{user_name}, you do not have an ID", "has_id": False}


# MULTIPLE QUERY PARAMS
@app.get("/is_license_valid")
async def is_license_valid(name: str, age: int) -> dict:
    if age >= 18:
        return {"message": f"{name}, your license is valid", "is_valid": True}
    else:
        return {"message": f"{name}, your license is not valid", "is_valid": False}
