"""Clerk authentication middleware"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from clerk_backend_api import Clerk

from app.config import settings
from app.database import get_db
from app.models import User

security = HTTPBearer()

clerk = Clerk(bearer_auth=settings.clerk_secret_key)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.

    - Verifies the Clerk JWT token using Clerk SDK
    - Gets or creates the user in our database
    - Returns the User object
    """
    token = credentials.credentials

    try:
        # Verify token using Clerk SDK
        verified_token = clerk.verify_token(token)
        clerk_user_id = verified_token.sub

        # Get user details from Clerk
        clerk_user = clerk.users.get(user_id=clerk_user_id)
        if not clerk_user:
            raise ValueError("User does not exist")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get or create user in our database
    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()

    if not user:
        # Create new user if doesn't exist
        email = None
        if clerk_user.email_addresses:
            email = clerk_user.email_addresses[0].email_address

        user = User(
            clerk_user_id=clerk_user_id,
            email=email or f"{clerk_user_id}@unknown.com"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user
