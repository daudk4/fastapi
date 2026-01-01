from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> dict:
    return {"message": "Hello root"}


@app.get("/greet/{user_name}")
async def greet_user(user_name: str) -> dict:
    return {"message": f"Welcome back {user_name}"}
