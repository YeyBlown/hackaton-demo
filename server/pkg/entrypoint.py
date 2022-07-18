"""main and only application entrypoint"""
import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from fastapi.middleware.cors import CORSMiddleware #cors

from adapters.contract import PostgresEnv, AppEnv

from controllers import auth, post, api, user


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(api.router)
app.include_router(user.router)

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=PostgresEnv.get_url())


# To run locally
if __name__ == "__main__":
    uvicorn.run(app, host=AppEnv.get_app_host(), port=AppEnv.get_app_port())
