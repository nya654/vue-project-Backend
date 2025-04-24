from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from Router.register import register
from settings import TORTOISE_ORM
from models import User
import uvicorn
from Router.login import router as login_router
from Router.register import register_router


app = FastAPI()


register_tortoise(
    app=app,

    config=TORTOISE_ORM,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 根据你的前端实际端口调整
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(login_router,tags=['login'])
app.include_router(register_router,tags=['注册模块'])

@app.get("/api/hello")
async def root():
    user = await User.get(id=2)
    print(user.email)
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)