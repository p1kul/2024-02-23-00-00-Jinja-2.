from fastapi import FastAPI,Path, status, Body, HTTPException, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def get_all(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html",{"request":request, "users":users})

@app.get(path="/users/{user_id}")
async def all_inf(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html",{"request":request, "user":users[user_id - 1]})

@app.post("/user/{username}/{age}")
async def create_message(user: User):
    if not users:
        user_id = 1
    else:
       user_id = users[-1].id + 1
    user.id = user_id
    users.append(user)
    return user

@app.put("/user/{user_id}/{username}/{age}")
async def refresh(user_id: int, username: str, age: int, user: str = Body()):
    try:
        users[user_id].username = username
        users[user_id].age = age
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")

@app.delete("/user/{user_id}")
async def delete(user_id: int) -> str:
    try:
        user = users.pop(user_id - 1)
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")








