import hashlib
import hmac
import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from database.connection import get_session
from models.users import NewUser, UserSignIn, UserAccount


user_router = APIRouter(tags=["User"])


def hash_password(password: str, salt: str) -> str:
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=bytes.fromhex(salt),
        n=16384,
        r=8,
        p=1,
    ).hex()


@user_router.post("/signup")
def sign_new_user(
    data: NewUser,
    session: Session = Depends(get_session),
):
    salt = secrets.token_hex(16)

    account = UserAccount(
        email=str(data.email),
        password_hash=f"{salt}:{hash_password(data.password, salt)}",
    )

    session.add(account)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="User with supplied email exists",
        )

    session.refresh(account)

    return {
        "message": "User successfully registered!",
        "user_id": account.id,
    }


@user_router.post("/signin")
def sign_user_in(
    user: UserSignIn,
    session: Session = Depends(get_session),
):
    account = session.exec(
        select(UserAccount).where(
            UserAccount.email == str(user.email)
        )
    ).first()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="User does not exist",
        )

    salt, saved_hash = account.password_hash.split(":", 1)
    entered_hash = hash_password(user.password, salt)

    if not hmac.compare_digest(entered_hash, saved_hash):
        raise HTTPException(
            status_code=403,
            detail="Wrong credentials passed",
        )

    return {"message": "User signed in successfully"}