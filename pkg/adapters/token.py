from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# TODO: move tokens to models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


# TODO: import user from models
class User(BaseModel):
    login: str


class UserInDB(User):
    hashed_password: str


app = FastAPI()


class TokenAdapter:

    # TODO: move hard variables to contract, please :)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = "5d8ff4f4a643f60dd33e0eeafb03fb8741578db760b4b4b08268041cd66d3195"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return TokenAdapter.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return TokenAdapter.pwd_context.hash(password)

    @staticmethod
    def get_user_by_username(db, username: str):
        # TODO: ask real db or just get user as param in higher function
        return None
        # if username in db:
        #     user_dict = db[username]
        #     return UserInDB(**user_dict)

    @staticmethod
    def authenticate_user(user, password: str):
        if not user:
            return False
        if not TokenAdapter.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, TokenAdapter.SECRET_KEY, algorithm=TokenAdapter.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, TokenAdapter.SECRET_KEY, algorithms=[TokenAdapter.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        # TODO: ask from db
        user = db.get_user(fake_users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    @staticmethod
    async def get_current_active_user(current_user: User = Depends(get_current_user)):
        # TODO: should i use class before last param?
        if current_user.disabled:  # TODO: should i add disabled to user BaseModel or token BaseModel?
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

# TODO: create token controllers in appropriate place
# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=TokenAdapter.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     return current_user
#
#
# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]
