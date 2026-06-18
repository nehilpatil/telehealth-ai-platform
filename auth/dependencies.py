# from jose import jwt

# from fastapi import Depends
# from fastapi.security import OAuth2PasswordBearer

# from auth.jwt_handler import (
#     SECRET_KEY,
#     ALGORITHM
# )

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="login"
# )

# def get_current_user(
#     token: str = Depends(oauth2_scheme)
# ):
#     payload = jwt.decode(
#         token,
#         SECRET_KEY,
#         algorithms=[ALGORITHM]
#     )

#     return payload

from jose import jwt

from fastapi import Header, HTTPException

from fastapi import HTTPException


def require_admin(current_user):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user

from auth.jwt_handler import (
    SECRET_KEY,
    ALGORITHM
)

def get_current_user(
    authorization: str = Header(None)
):
    print(repr(authorization))

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing token"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload

